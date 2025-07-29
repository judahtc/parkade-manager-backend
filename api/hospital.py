from datetime import datetime
from fastapi import FastAPI, APIRouter, HTTPException
from db.database import SessionLocal, engine, get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from models import models
from schemas import schemas

router = APIRouter(prefix="/hospital", tags=["hospital"])


@router.get("/")
def get_hospitals(db: Session = Depends(get_db)):
    hospitals = db.query(models.Hospital).all()
    return hospitals


@router.get("/{hospital_id}")
def get_hospital(hospital_id: int, db: Session = Depends(get_db)):
    hospital = db.query(models.Hospital).filter(
        models.Hospital.id == hospital_id).first()
    if not hospital:
        raise HTTPException(status_code=404, detail="Hospital not found")
    return hospital


@router.delete("/{hospital_id}")
def delete_hospital(hospital_id: int, db: Session = Depends(get_db)):
    db_hospital = db.query(models.Hospital).filter(
        models.Hospital.id == hospital_id).first()
    if not db_hospital:
        raise HTTPException(status_code=404, detail="Hospital not found")

    db.delete(db_hospital)
    db.commit()
    return {"detail": "Hospital deleted successfully"}


@router.post("/")
def create_hospital(hospital: schemas.HospitalCreate, db: Session = Depends(get_db)):
    new_hospital = models.Hospital(

        name=hospital.name,
        address=hospital.address,
        contact_number=hospital.contact_number,
        email=hospital.email,
        website=hospital.website
    )
    db.add(new_hospital)
    db.commit()
    db.refresh(new_hospital)
    return new_hospital


@router.put("/{hospital_id}")
def update_hospital(hospital_id: int, hospital: schemas.HospitalUpdate, db: Session = Depends(get_db)):
    db_hospital = db.query(models.Hospital).filter(
        models.Hospital.id == hospital_id).first()
    if not db_hospital:
        raise HTTPException(status_code=404, detail="Hospital not found")

    for key, value in hospital.dict(exclude_unset=True).items():
        setattr(db_hospital, key, value)

    db.commit()
    db.refresh(db_hospital)
    return db_hospital
