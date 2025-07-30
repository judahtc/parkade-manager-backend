from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from models import models
from schemas import schemas
from typing import List

router = APIRouter(prefix="/payments", tags=["payments"])

@router.post("", response_model=schemas.PaymentResponse)
def create_payment(payment: schemas.PaymentCreate, db: Session = Depends(get_db)):
    car = db.query(models.Car).filter(models.Car.id == payment.car_id).first()
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    new_payment = models.Payment(**payment.dict())
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    return new_payment

@router.get("", response_model=List[schemas.PaymentResponse])
def get_all_payments(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(models.Payment).offset(skip).limit(limit).all()

@router.get("/{payment_id}", response_model=schemas.PaymentResponse)
def get_payment(payment_id: int, db: Session = Depends(get_db)):
    payment = db.query(models.Payment).filter(models.Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment

@router.put("/{payment_id}", response_model=schemas.PaymentResponse)
def update_payment(payment_id: int, update: schemas.PaymentUpdate, db: Session = Depends(get_db)):
    payment = db.query(models.Payment).filter(models.Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    for key, value in update.dict(exclude_unset=True).items():
        setattr(payment, key, value)
    db.commit()
    db.refresh(payment)
    return payment

@router.delete("/{payment_id}")
def delete_payment(payment_id: int, db: Session = Depends(get_db)):
    payment = db.query(models.Payment).filter(models.Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    db.delete(payment)
    db.commit()
    return {"detail": "Payment deleted successfully"}
