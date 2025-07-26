from __future__ import annotations
from datetime import date
from typing import List, Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base

class Company(Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True)
    address: Mapped[Optional[str]]
    contact_person: Mapped[Optional[str]]
    phone_number: Mapped[Optional[str]]

    users: Mapped[List["User"]] = relationship(back_populates="company")
    farmers: Mapped[List["Farmer"]] = relationship(back_populates="company")

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str]
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    full_name: Mapped[Optional[str]]
    disabled: Mapped[bool] = mapped_column(default=False)
    role: Mapped[str] = mapped_column(default="agent")
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"))

    company: Mapped["Company"] = relationship(back_populates="users")

class Farmer(Base):
    __tablename__ = "farmers"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(index=True)
    village: Mapped[str]
    mobile_number: Mapped[str] = mapped_column(String, unique=True, index=True)
    aadhaar_number: Mapped[Optional[str]] = mapped_column(String, unique=True)
    farm_area_acres: Mapped[float]
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"))

    company: Mapped["Company"] = relationship(back_populates="farmers")
    seed_distributions: Mapped[List["SeedDistribution"]] = relationship(back_populates="farmer")
    harvest_entries: Mapped[List["HarvestEntry"]] = relationship(back_populates="farmer")
    receipts: Mapped[List["Receipt"]] = relationship(back_populates="farmer")

class SeedDistribution(Base):
    __tablename__ = "seed_distributions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    farmer_id: Mapped[int] = mapped_column(ForeignKey("farmers.id"))
    date: Mapped[date]
    num_bags_given: Mapped[int]
    rate_per_bag: Mapped[float]
    total_amount: Mapped[float]

    farmer: Mapped["Farmer"] = relationship(back_populates="seed_distributions")

class HarvestEntry(Base):
    __tablename__ = "harvest_entries"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    farmer_id: Mapped[int] = mapped_column(ForeignKey("farmers.id"))
    date: Mapped[date]
    num_bags_returned: Mapped[int]
    net_weight_per_bag_kg: Mapped[float]
    total_weight_quintals: Mapped[float]
    rate_per_quintal: Mapped[float]
    total_amount: Mapped[float]

    farmer: Mapped["Farmer"] = relationship(back_populates="harvest_entries")

class Receipt(Base):
    __tablename__ = "receipts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    farmer_id: Mapped[int] = mapped_column(ForeignKey("farmers.id"))
    date: Mapped[date]
    seed_cost_debit: Mapped[float]
    rice_sale_credit: Mapped[float]
    final_balance: Mapped[float]

    farmer: Mapped["Farmer"] = relationship(back_populates="receipts")
