from datetime import datetime, timedelta, timezone

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    JSON,
    ARRAY,
    Date, UUID, Text, TIMESTAMP
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from db.database import RDS_DB_SCHEMA, Base


class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    role = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now,
                        onupdate=datetime.now, nullable=False)
    is_active = Column(Boolean, default=True)
    hospital_id = Column(Integer, ForeignKey("hospitals.id"), nullable=False)
    hospital = relationship("Hospital", back_populates="admins")


class Hospital(Base):
    __tablename__ = "hospitals"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    contact_number = Column(String, nullable=False)
    email = Column(String, nullable=False)
    website = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now,
                        nullable=False)
    admins = relationship("Admin", back_populates="hospital")
    patients = relationship("Patient", back_populates="hospital")


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(Text, nullable=False)  # Use a hashed password
    next_of_kin_email = Column(String, nullable=True)
    ward_number = Column(String, nullable=False)
    room_number = Column(String, nullable=False)
    discharged=Column(Boolean,default=False)
    checkin_date = Column(TIMESTAMP, nullable=False, default=datetime.now())
    checkout_date = Column(TIMESTAMP, nullable=True)
    hospital_id = Column(Integer, ForeignKey("hospitals.id"), nullable=False)
    hospital = relationship("Hospital", back_populates="patients")
    visitors = relationship("Visitor", back_populates="patients")


class Visitor(Base):
    __tablename__ = "visitors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    national_id = Column(String, unique=True, nullable=False)
    visited = Column(Boolean,  default=False)
    visit_date = Column(DateTime, nullable=False)
    patient_id = Column(Integer,
                        ForeignKey("patients.id"), nullable=False)
    patients = relationship("Patient", back_populates="visitors")
