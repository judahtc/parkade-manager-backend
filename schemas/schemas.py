from pydantic import BaseModel, EmailStr
from typing import Optional, Union, Any
from uuid import UUID
from datetime import datetime


class HospitalBase(BaseModel):
    name: str
    address: str
    contact_number: str
    email: EmailStr
    website: Optional[str] = None


class HospitalCreate(HospitalBase):
    pass


class HospitalUpdate(HospitalBase):
    name: Optional[str] = None
    address: Optional[str] = None
    contact_number: Optional[str] = None
    email: Optional[EmailStr] = None
    website: Optional[str] = None


class HospitalRead(HospitalBase):
    id: int
    created_at: datetime
    updated_at: datetime


class AdminBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    role: str
    hospital_id: int
    is_active: bool = True


class AdminCreate(AdminBase):
    password: str


class AdminUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    phone_number: str | None = None
    role: str | None = None
    is_active: bool | None = None


class AdminResponse(AdminBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Pydantic Models


class PatientBase(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    email: str
    next_of_kin_email: EmailStr | None = None
    ward_number: str
    room_number: Optional[str] = None
    checkin_date:  datetime | None = None
    checkout_date: datetime | None = None
    hospital_id: int| None = None
    discharged: bool| None = None


class PatientCreate(PatientBase):
    password: str | None = None


class PatientUpdate(BaseModel):
    
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None
    next_of_kin_email: Optional[EmailStr] = None
    ward_number: Optional[str] = None
    room_number: Optional[str] = None
    discharged: bool| None = None
    checkin_date: Optional[datetime] = None
    checkout_date: Optional[datetime] = None
    hospital_id: Optional[int] = None


class PatientResponse(PatientBase):
    name: Optional[str] = None
    patient_visitors: list[Any]| None = None
    id: int

    class Config:
        orm_mode = True


class VisitorBase(BaseModel):
    name: str
    national_id: str
    visited: bool = False
    visit_date: datetime
    patient_id: int


class VisitorCreate(VisitorBase):
    pass


class VisitorUpdate(BaseModel):
    name: Optional[str] = None
    national_id: Optional[str] = None
    visited: Optional[bool] = None
    visit_date: Optional[datetime] = None
    patient_id: Optional[int] = None


class VisitorResponse(VisitorBase):
    id: int

    class Config:
        orm_mode = True


class LoginSchema(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: str
