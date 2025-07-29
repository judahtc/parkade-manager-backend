from fastapi import FastAPI, APIRouter
from fastapi import Depends, HTTPException
from models import models
from schemas import schemas
from db.database import SessionLocal, engine, get_db
from sqlalchemy.orm import Session
from typing import List, Union
import sqlalchemy
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
router = APIRouter(prefix="/admin", tags=["admin"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ------------------------------------- Create Admins --------------------------------------------------


@router.post("/", response_model=schemas.AdminResponse)
def create_admin(admin: schemas.AdminCreate, db: Session = Depends(get_db)):
    db_admin = db.query(models.Admin).filter(
        models.Admin.email == admin.email).first()
    if db_admin:

        raise HTTPException(status_code=400, detail="Email already registered")
    try:

        admin_data = admin.dict()
        my_hashed_password = pwd_context.hash(admin.password)
        admin_data['password'] = my_hashed_password
        new_admin = models.Admin(**admin_data)

        db.add(new_admin)

        db.commit()
        db.refresh(new_admin)
        return new_admin
    except sqlalchemy.exc.IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=400, detail=str(e.orig))
# ------------------------------------- Read All Admins --------------------------------------------------


@router.get("/", response_model=List[schemas.AdminResponse])
def read_admins(db: Session = Depends(get_db)):
    admins = db.query(models.Admin).all()
    return admins

# -------------------------------------------------- Read Single Admin --------------------------------------------------


@router.get("/{admin_id}", response_model=schemas.AdminResponse)
def read_admin(admin_id: int, db: Session = Depends(get_db)):
    admin = db.query(models.Admin).filter(models.Admin.id == admin_id).first()
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    return admin

# -------------------------------------------------- Update Admin --------------------------------------------------


@router.put("/{admin_id}", response_model=schemas.AdminResponse)
def update_admin(admin_id: int, admin_update: schemas.AdminUpdate, db: Session = Depends(get_db)):
    admin = db.query(models.Admin).filter(models.Admin.id == admin_id).first()
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    for key, value in admin_update.dict(exclude_unset=True).items():
        setattr(admin, key, value)
    db.commit()
    db.refresh(admin)
    return admin

# -------------------------------------------------- Delete Admin --------------------------------------------------


@router.delete("/{admin_id}", response_model=dict)
def delete_admin(admin_id: int, db: Session = Depends(get_db)):
    admin = db.query(models.Admin).filter(models.Admin.id == admin_id).first()
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    db.delete(admin)
    db.commit()
    return {"detail": "Admin deleted successfully"}
