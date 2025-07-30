from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey,Numeric
from sqlalchemy.orm import relationship
from datetime import datetime
from db.database import Base  # Make sure you import your declarative base

class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)
    plate_number = Column(String, unique=True, nullable=False, index=True)
    owner_name = Column(String, nullable=False)
    owner_email = Column(String, nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    is_active = Column(Boolean, default=True)
    registered_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    company = relationship("Company", back_populates="cars")
    payments = relationship("Payment", back_populates="car")


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    address = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    cars = relationship("Car", back_populates="company")

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    car_id = Column(Integer, ForeignKey("cars.id"), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    month_paid = Column(DateTime, nullable=False)  # You could use just `Date` if month granularity is enough
    paid_on = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="paid")  # paid, unpaid, pending

    # Relationship
    car = relationship("Car", back_populates="payments")
 