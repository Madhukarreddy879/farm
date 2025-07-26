from sqlalchemy.orm import Session
from datetime import date
from typing import List, Optional

from . import models, schemas
from .auth import get_password_hash

# --- Company Operations ---
def get_company(db: Session, company_id: int):
    return db.query(models.Company).filter(models.Company.id == company_id).first()

def get_company_by_name(db: Session, name: str):
    return db.query(models.Company).filter(models.Company.name == name).first()

def get_companies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Company).offset(skip).limit(limit).all()

def create_company(db: Session, company: schemas.CompanyCreate):
    db_company = models.Company(**company.model_dump())
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company

def update_company(db: Session, company_id: int, company: schemas.CompanyUpdate):
    db_company = get_company(db, company_id)
    if db_company:
        update_data = company.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_company, key, value)
        db.add(db_company)
        db.commit()
        db.refresh(db_company)
    return db_company

def delete_company(db: Session, company_id: int):
    db_company = get_company(db, company_id)
    if db_company:
        db.delete(db_company)
        db.commit()
    return db_company

# --- User Operations ---
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password,
        role=user.role,
        company_id=user.company_id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate):
    db_user = get_user(db, user_id)
    if db_user:
        update_data = user_update.model_dump(exclude_unset=True)
        if "password" in update_data and update_data["password"]:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
        for key, value in update_data.items():
            setattr(db_user, key, value)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user

# --- Farmer Operations ---
def get_farmer(db: Session, farmer_id: int):
    return db.query(models.Farmer).filter(models.Farmer.id == farmer_id).first()

def get_farmers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Farmer).offset(skip).limit(limit).all()

def get_farmers_by_company(db: Session, company_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Farmer).filter(models.Farmer.company_id == company_id).offset(skip).limit(limit).all()

def get_farmer_by_mobile_number(db: Session, mobile_number: str, company_id: int):
    return db.query(models.Farmer).filter(
        models.Farmer.mobile_number == mobile_number,
        models.Farmer.company_id == company_id
    ).first()

def create_farmer(db: Session, farmer: schemas.FarmerCreate):
    db_farmer = models.Farmer(**farmer.model_dump())
    db.add(db_farmer)
    db.commit()
    db.refresh(db_farmer)
    return db_farmer

def update_farmer(db: Session, farmer_id: int, farmer_update: schemas.FarmerUpdate):
    db_farmer = get_farmer(db, farmer_id)
    if db_farmer:
        update_data = farmer_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_farmer, key, value)
        db.add(db_farmer)
        db.commit()
        db.refresh(db_farmer)
    return db_farmer

def delete_farmer(db: Session, farmer_id: int):
    db_farmer = get_farmer(db, farmer_id)
    if db_farmer:
        db.delete(db_farmer)
        db.commit()
    return db_farmer

# --- Seed Distribution Operations ---
def get_seed_distribution(db: Session, sd_id: int):
    return db.query(models.SeedDistribution).filter(models.SeedDistribution.id == sd_id).first()

def get_seed_distributions_by_farmer(db: Session, farmer_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.SeedDistribution).filter(
        models.SeedDistribution.farmer_id == farmer_id
    ).offset(skip).limit(limit).all()

def create_seed_distribution(db: Session, seed_dist: schemas.SeedDistributionCreate):
    total_amount = seed_dist.num_bags_given * seed_dist.rate_per_bag
    db_seed_dist = models.SeedDistribution(
        **seed_dist.model_dump(),
        total_amount=total_amount
    )
    db.add(db_seed_dist)
    db.commit()
    db.refresh(db_seed_dist)
    return db_seed_dist

# --- Harvest Entry Operations ---
def get_harvest_entry(db: Session, he_id: int):
    return db.query(models.HarvestEntry).filter(models.HarvestEntry.id == he_id).first()

def get_harvest_entries_by_farmer(db: Session, farmer_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.HarvestEntry).filter(
        models.HarvestEntry.farmer_id == farmer_id
    ).offset(skip).limit(limit).all()

def create_harvest_entry(db: Session, harvest_entry: schemas.HarvestEntryCreate):
    total_weight_quintals = (harvest_entry.num_bags_returned * harvest_entry.net_weight_per_bag_kg) / 100
    total_amount = total_weight_quintals * harvest_entry.rate_per_quintal
    db_harvest_entry = models.HarvestEntry(
        **harvest_entry.model_dump(),
        total_weight_quintals=total_weight_quintals,
        total_amount=total_amount
    )
    db.add(db_harvest_entry)
    db.commit()
    db.refresh(db_harvest_entry)
    return db_harvest_entry

# --- Receipt Operations ---
def get_receipt(db: Session, receipt_id: int):
    return db.query(models.Receipt).filter(models.Receipt.id == receipt_id).first()

def get_receipts_by_farmer(db: Session, farmer_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Receipt).filter(
        models.Receipt.farmer_id == farmer_id
    ).offset(skip).limit(limit).all()

def calculate_and_create_receipt(db: Session, farmer_id: int, receipt_date: date):
    farmer = get_farmer(db, farmer_id)
    if not farmer:
        return None

    seed_distributions = get_seed_distributions_by_farmer(db, farmer_id)
    harvest_entries = get_harvest_entries_by_farmer(db, farmer_id)

    total_seed_cost_debit = sum(sd.total_amount for sd in seed_distributions)
    total_rice_sale_credit = sum(he.total_amount for he in harvest_entries)

    final_balance = total_rice_sale_credit - total_seed_cost_debit

    db_receipt = models.Receipt(
        farmer_id=farmer_id,
        date=receipt_date,
        seed_cost_debit=total_seed_cost_debit,
        rice_sale_credit=total_rice_sale_credit,
        final_balance=final_balance
    )
    db.add(db_receipt)
    db.commit()
    db.refresh(db_receipt)
    return db_receipt
