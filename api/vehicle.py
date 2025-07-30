from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from models import models
from schemas import schemas
from typing import List

router = APIRouter(prefix="/cars", tags=["cars"])

# Get all cars
@router.get("", response_model=List[schemas.CarResponse])
def get_all_cars(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    cars = db.query(models.Car).offset(skip).limit(limit).all()
    return cars

# Get a single car by ID
@router.get("/{car_id}", response_model=schemas.CarResponse)
def get_car(car_id: int, db: Session = Depends(get_db)):
    car = db.query(models.Car).filter(models.Car.id == car_id).first()
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    return car

# Create a new car
@router.post("", response_model=schemas.CarResponse)
def create_car(car: schemas.CarCreate, db: Session = Depends(get_db)):
    existing_car = db.query(models.Car).filter(
        models.Car.plate_number == car.plate_number).first()
    if existing_car:
        raise HTTPException(status_code=400, detail="Car with this plate number already exists")
    new_car = models.Car(**car.dict())
    db.add(new_car)
    db.commit()
    db.refresh(new_car)
    return new_car

# Update a car
@router.put("/{car_id}", response_model=schemas.CarResponse)
def update_car(car_id: int, car_update: schemas.CarUpdate, db: Session = Depends(get_db)):
    car = db.query(models.Car).filter(models.Car.id == car_id).first()
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    for key, value in car_update.dict(exclude_unset=True).items():
        setattr(car, key, value)
    db.commit()
    db.refresh(car)
    return car

# Delete a car
@router.delete("/{car_id}", response_model=dict)
def delete_car(car_id: int, db: Session = Depends(get_db)):
    car = db.query(models.Car).filter(models.Car.id == car_id).first()
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    db.delete(car)
    db.commit()
    return {"detail": "Car deleted successfully"}

# Get a car by plate number
@router.get("/by-plate/{plate_number}", response_model=schemas.CarResponse)
def get_car_by_plate(plate_number: str, db: Session = Depends(get_db)):
    car = db.query(models.Car).filter(models.Car.plate_number == plate_number).first()
    if not car:
        raise HTTPException(status_code=404, detail="Car not found with given plate number")
    return car
