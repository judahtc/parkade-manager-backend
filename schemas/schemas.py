from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class CarBase(BaseModel):
    plate_number: str
    owner_name: str
    owner_email: EmailStr
    company_id: int
    is_active: Optional[bool] = True
    registered_at: Optional[datetime] = None

class CarCreate(CarBase):
    pass  # Use the same fields as CarBase when creating

class CarUpdate(BaseModel):
    plate_number: Optional[str] = None
    owner_name: Optional[str] = None
    owner_email: Optional[EmailStr] = None
    company_id: Optional[int] = None
    is_active: Optional[bool] = None
    registered_at: Optional[datetime] = None

class CarResponse(CarBase):
    id: int

    class Config:
        orm_mode = True


class LoginSchema(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: str


class CompanyBase(BaseModel):
    name: str
    email: EmailStr
    address: Optional[str] = None
    phone: Optional[str] = None

class CompanyCreate(CompanyBase):
    pass

class CompanyUpdate(CompanyBase):
    pass

class CompanyResponse(CompanyBase):
    id: int
    created_at: datetime


    class Config:
        orm_mode = True
