from fastapi import FastAPI, APIRouter
from fastapi import Depends, HTTPException
from models import models
from schemas import schemas
from db.database import SessionLocal, engine, get_db
from sqlalchemy.orm import Session
from typing import List, Union


router = APIRouter(prefix="/visitors", tags=["drivers"])


@router.get("/")
def get_visitors(db:Session= Depends(get_db)):
    visitors=db.query(models.Visitor).all()
    return visitors

# Create Visitor


@router.post("/", response_model=schemas.VisitorResponse)
def create_visitor(visitor: schemas.VisitorCreate, db: Session = Depends(get_db)):
    db_visitor = db.query(models.Visitor).filter(
        models.Visitor.national_id == visitor.national_id).first()
    if db_visitor:
        raise HTTPException(
            status_code=400, detail="National ID already registered")
    new_visitor = models.Visitor(**visitor.dict())
    db.add(new_visitor)
    db.commit()
    db.refresh(new_visitor)
    return new_visitor

# Get All Visitors


@router.get("/", response_model=List[schemas.VisitorResponse])
def read_visitors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    visitors = db.query(models.Visitor).all()
    return visitors

# Get Single Visitor by ID


@router.get("/{visitor_id}", response_model=schemas.VisitorResponse)
def read_visitor(visitor_id: int, db: Session = Depends(get_db)):
    visitor = db.query(models.Visitor).filter(
        models.Visitor.id == visitor_id).first()
    if not visitor:
        raise HTTPException(status_code=404, detail="Visitor not found")
    return visitor

# Query Visitor by National ID


@router.get("/by-national-id/{national_id}", response_model=schemas.VisitorResponse)
def get_visitor_by_national_id(national_id: str, db: Session = Depends(get_db)):
    visitor = db.query(models.Visitor).filter(
        models.Visitor.national_id == national_id).first()
    if not visitor:
        raise HTTPException(
            status_code=404, detail="Visitor not found with the given National ID")
    return visitor

# Update Visitor


@router.put("/{visitor_id}", response_model=schemas.VisitorResponse)
def update_visitor(visitor_id: int, visitor_update: schemas.VisitorUpdate, db: Session = Depends(get_db)):
    visitor = db.query(models.Visitor).filter(
        models.Visitor.id == visitor_id).first()
    if not visitor:
        raise HTTPException(status_code=404, detail="Visitor not found")
    for key, value in visitor_update.dict(exclude_unset=True).items():
        setattr(visitor, key, value)
    db.commit()
    db.refresh(visitor)
    return visitor

# Delete Visitor


@router.delete("/{visitor_id}", response_model=dict)
def delete_visitor(visitor_id: int, db: Session = Depends(get_db)):
    visitor = db.query(models.Visitor).filter(
        models.Visitor.id == visitor_id).first()
    if not visitor:
        raise HTTPException(status_code=404, detail="Visitor not found")
    db.delete(visitor)
    db.commit()
    return {"detail": "Visitor deleted successfully"}


@router.put("/{visitor_id}", response_model=dict)
def check_in_visitor(visitor_id: int, db: Session = Depends(get_db)):
    visitor = db.query(models.Visitor).filter(
        models.Visitor.id == visitor_id).first()
    if not visitor:
        raise HTTPException(status_code=404, detail="Visitor not found")
    

    # CHECK IN CODE
    db.commit()
    return {"detail": "Visitor checked in successfully"}
@router.put("/{visitor_id}/re_check_in", response_model=dict)
def re_check_in_visitor(visitor_id: int, db: Session = Depends(get_db)):
    visitor = db.query(models.Visitor).filter(
        models.Visitor.id == visitor_id).first()
    if not visitor:
        raise HTTPException(status_code=404, detail="Visitor not found")
    

    # CHECK IN CODE
    db.commit()
    return {"detail": "Visitor checked in successfully"}


