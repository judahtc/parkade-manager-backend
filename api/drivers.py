from fastapi import FastAPI, APIRouter
from fastapi import Depends, HTTPException
from models import models
from schemas import schemas
from db.database import SessionLocal, engine, get_db
from sqlalchemy.orm import Session
from typing import List, Union


router = APIRouter(prefix="/drivers", tags=["drivers"])


@router.get("/")
def get_drivers(db:Session= Depends(get_db)):
    drivers=db.query(models.Driver).all()
    return drivers

# Create Driver


@router.post("/", response_model=schemas.DriverResponse)
def create_driver(driver: schemas.DriverCreate, db: Session = Depends(get_db)):
    db_driver = db.query(models.Driver).filter(
        models.Driver.national_id == driver.national_id).first()
    if db_driver:
        raise HTTPException(
            status_code=400, detail="National ID already registered")
    new_driver = models.Driver(**driver.dict())
    db.add(new_driver)
    db.commit()
    db.refresh(new_driver)
    return new_driver

# Get All Drivers


@router.get("/", response_model=List[schemas.DriverResponse])
def read_drivers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    drivers = db.query(models.Driver).all()
    return drivers

# Get Single Driver by ID


@router.get("/{driver_id}", response_model=schemas.DriverResponse)
def read_driver(driver_id: int, db: Session = Depends(get_db)):
    driver = db.query(models.Driver).filter(
        models.Driver.id == driver_id).first()
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    return driver

# Query Driver by National ID


@router.get("/by-national-id/{national_id}", response_model=schemas.DriverResponse)
def get_driver_by_national_id(national_id: str, db: Session = Depends(get_db)):
    driver = db.query(models.Driver).filter(
        models.Driver.national_id == national_id).first()
    if not driver:
        raise HTTPException(
            status_code=404, detail="Driver not found with the given National ID")
    return driver

# Update Driver


@router.put("/{driver_id}", response_model=schemas.DriverResponse)
def update_driver(driver_id: int, driver_update: schemas.DriverUpdate, db: Session = Depends(get_db)):
    driver = db.query(models.Driver).filter(
        models.Driver.id == driver_id).first()
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    for key, value in driver_update.dict(exclude_unset=True).items():
        setattr(driver, key, value)
    db.commit()
    db.refresh(driver)
    return driver

# Delete Driver


@router.delete("/{driver_id}", response_model=dict)
def delete_driver(driver_id: int, db: Session = Depends(get_db)):
    driver = db.query(models.Driver).filter(
        models.Driver.id == driver_id).first()
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    db.delete(driver)
    db.commit()
    return {"detail": "Driver deleted successfully"}


@router.put("/{driver_id}/check-in", response_model=dict)
def check_in_driver(driver_id: int, db: Session = Depends(get_db)):
    driver = db.query(models.Driver).filter(
        models.Driver.id == driver_id).first()
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    

    # CHECK IN CODE
    db.commit()
    return {"detail": "Driver checked in successfully"}
@router.put("/{driver_id}/re-check-in", response_model=dict)
def re_check_in_driver(driver_id: int, db: Session = Depends(get_db)):
    driver = db.query(models.Driver).filter(
        models.Driver.id == driver_id).first()
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    

    # CHECK IN CODE
    db.commit()
    return {"detail": "Driver checked in successfully"}


