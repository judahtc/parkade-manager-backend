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
