from datetime import timedelta, date
from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from . import crud, models, schemas, auth
from .database import engine, get_db
from .config import settings

# Create all database tables.
# This should ideally be handled by a migration tool like Alembic in production.
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Rice Mill B2B Application API",
    description="API for managing rice mill operations, farmer data, seed distribution, harvest entries, and receipts.",
    version="1.0.0",
)

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    Authenticate user and return an access token.
    """
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=schemas.User)
async def read_users_me(current_user: models.User = Depends(auth.get_current_active_user)):
    """
    Get the details of the currently authenticated user.
    """
    return current_user

# --- Company Endpoints ---
@app.post("/companies/", response_model=schemas.Company, status_code=status.HTTP_201_CREATED)
async def create_company(
    company: schemas.CompanyCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_admin_user)
):
    """
    Create a new company. (Admin only)
    """
    db_company = crud.get_company_by_name(db, name=company.name)
    if db_company:
        raise HTTPException(status_code=400, detail="Company name already registered")
    return crud.create_company(db=db, company=company)

@app.get("/companies/", response_model=List[schemas.Company])
async def read_companies(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_admin_user)
):
    """
    Retrieve a list of companies. (Admin only)
    """
    companies = crud.get_companies(db, skip=skip, limit=limit)
    return companies

# --- User Endpoints ---
@app.post("/users/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_admin_user)
):
    """
    Create a new user for a company. (Admin only)
    """
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    db_user_email = crud.get_user_by_email(db, email=user.email)
    if db_user_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    company = crud.get_company(db, user.company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    return crud.create_user(db=db, user=user)

# --- Farmer Endpoints ---
@app.post("/farmers/", response_model=schemas.Farmer, status_code=status.HTTP_201_CREATED)
async def create_farmer(
    farmer: schemas.FarmerCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_agent_user)
):
    """
    Register a new farmer.
    """
    if current_user.role in ["agent", "company_owner"] and farmer.company_id != current_user.company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot create farmer for a different company."
        )

    db_farmer = crud.get_farmer_by_mobile_number(db, mobile_number=farmer.mobile_number, company_id=farmer.company_id)
    if db_farmer:
        raise HTTPException(status_code=400, detail="Farmer with this mobile number already registered for this company.")

    return crud.create_farmer(db=db, farmer=farmer)

@app.get("/farmers/", response_model=List[schemas.Farmer])
async def read_farmers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_agent_user)
):
    """
    Retrieve a list of farmers for the user's company. Admins can see all.
    """
    if current_user.role == "admin":
        farmers = crud.get_farmers(db, skip=skip, limit=limit)
    else:
        farmers = crud.get_farmers_by_company(db, company_id=current_user.company_id, skip=skip, limit=limit)
    return farmers

# --- Seed Distribution Endpoints ---
@app.post("/seed-distributions/", response_model=schemas.SeedDistribution, status_code=status.HTTP_201_CREATED)
async def create_seed_distribution(
    seed_dist: schemas.SeedDistributionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_agent_user)
):
    """
    Create a new seed distribution entry for a farmer.
    """
    farmer = crud.get_farmer(db, farmer_id=seed_dist.farmer_id)
    if not farmer:
        raise HTTPException(status_code=404, detail="Farmer not found")

    if current_user.role != "admin" and farmer.company_id != current_user.company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot add entry for a farmer outside your company."
        )

    return crud.create_seed_distribution(db=db, seed_dist=seed_dist)

# --- Harvest Entry Endpoints ---
@app.post("/harvest-entries/", response_model=schemas.HarvestEntry, status_code=status.HTTP_201_CREATED)
async def create_harvest_entry(
    harvest_entry: schemas.HarvestEntryCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_agent_user)
):
    """
    Create a new harvest entry for a farmer.
    """
    farmer = crud.get_farmer(db, farmer_id=harvest_entry.farmer_id)
    if not farmer:
        raise HTTPException(status_code=404, detail="Farmer not found")

    if current_user.role != "admin" and farmer.company_id != current_user.company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot add entry for a farmer outside your company."
        )

    return crud.create_harvest_entry(db=db, harvest_entry=harvest_entry)

# --- Receipt Endpoints ---
@app.post("/farmers/{farmer_id}/receipts/", response_model=schemas.Receipt, status_code=status.HTTP_201_CREATED)
async def generate_farmer_receipt(
    farmer_id: int,
    receipt_date: date,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_agent_user)
):
    """
    Generate a new receipt for a farmer based on their transaction history.
    """
    farmer = crud.get_farmer(db, farmer_id=farmer_id)
    if not farmer:
        raise HTTPException(status_code=404, detail="Farmer not found")

    if current_user.role != "admin" and farmer.company_id != current_user.company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot generate receipt for a farmer outside your company."
        )

    receipt = crud.calculate_and_create_receipt(db, farmer_id=farmer_id, receipt_date=receipt_date)
    if not receipt:
        raise HTTPException(status_code=500, detail="Failed to generate receipt.")
    return receipt

@app.get("/farmers/{farmer_id}/receipts/", response_model=List[schemas.Receipt])
async def get_farmer_receipts(
    farmer_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_agent_user)
):
    """
    Retrieve all receipts for a specific farmer.
    """
    farmer = crud.get_farmer(db, farmer_id=farmer_id)
    if not farmer:
        raise HTTPException(status_code=404, detail="Farmer not found")

    if current_user.role != "admin" and farmer.company_id != current_user.company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to view receipts for this farmer."
        )

    return crud.get_receipts_by_farmer(db, farmer_id=farmer_id, skip=skip, limit=limit)
