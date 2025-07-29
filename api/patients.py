
from fastapi import FastAPI, APIRouter
from fastapi import Depends, HTTPException
from models import models
from schemas import schemas
from db.database import SessionLocal, engine, get_db
from sqlalchemy.orm import Session
from typing import List, Union


router = APIRouter(prefix="/patients", tags=["patients"])


# Create Patient
@router.post("/", response_model=schemas.PatientResponse)
def create_patient(patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    db_patient = db.query(models.Patient).filter(
        models.Patient.email == patient.email).first()
    if db_patient:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_patient = models.Patient(**patient.dict())
    new_patient.hospital_id=1
    new_patient.password="password_to_be_hashed"
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    return new_patient

# Get All Patients


@router.get("/", response_model=List[schemas.PatientResponse])
def read_patients(db: Session = Depends(get_db)):
    patients = db.query(models.Patient).all()

    for patient in patients:
        
        patient.name=patient.first_name+' '+patient.last_name
        print(patient.name)

    patients=sorted(patients, key=lambda x: x.checkin_date, reverse=True)

    return patients

# Get Single Patient by ID


@router.get("/{email}", response_model=schemas.PatientResponse)
def read_patient(email: str, db: Session = Depends(get_db)):
    patient = db.query(models.Patient).filter(
        models.Patient.email == email).first()
    patient.name=patient.first_name+' '+patient.last_name
    visitors=db.query(models.Visitor).filter(models.Visitor.patient_id == patient.id).all()
    visitor_ids=[]
    for visitor in visitors:
        visitor_dict = {
            "id": visitor.id,
            "name": visitor.name,
            "patient_id": visitor.national_id,
            "visited": visitor.visited,
        
        }
        visitor_ids.append(visitor_dict)
       

    patient.patient_visitors=visitor_ids
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    return patient
@router.get("/patient/{id}")
def read_patient_by_id(id: int, db: Session = Depends(get_db)):
    patient = db.query(models.Patient).filter(
        models.Patient.id == id).first()
  
    return {"email":patient.email}

# Update Patient


@router.put("/{patient_id}", response_model=schemas.PatientResponse)
def update_patient(patient_id: int, patient_update: schemas.PatientUpdate, db: Session = Depends(get_db)):
    patient = db.query(models.Patient).filter(
        models.Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    for key, value in patient_update.dict(exclude_unset=True).items():
        setattr(patient, key, value)
    db.commit()
    db.refresh(patient)
    return patient

# Delete Patient


@router.delete("/{patient_id}", response_model=dict)
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(models.Patient).filter(
        models.Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    db.delete(patient)
    db.commit()
    return {"detail": "Patient deleted successfully"}
@router.put("/{patient_id}", response_model=dict)
def discharge_patient(patient_id: int, db: Session = Depends(get_db)):

    patient = db.query(models.Patient).filter(
        models.Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    patient.discharged=True
    db.commit()
    return {"detail": "Patient discharged successfully"}


