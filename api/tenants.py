from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from db.database import get_db
from models import models
from schemas import schemas

router = APIRouter(prefix="/tenants", tags=["tenants"])

@router.post("", response_model=schemas.TenantResponse, status_code=status.HTTP_201_CREATED)
def create_tenant(payload: schemas.TenantCreate, db: Session = Depends(get_db)):
    exists = db.query(models.Tenant).filter(models.Tenant.name == payload.name).first()
    if exists:
        raise HTTPException(status_code=400, detail="Tenant with this name already exists")
    tenant = models.Tenant(**payload.dict())
    db.add(tenant)
    db.commit()
    db.refresh(tenant)
    return tenant

@router.get("", response_model=List[schemas.TenantResponse])
def list_tenants(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return db.query(models.Tenant).offset(skip).limit(limit).all()

@router.get("/{tenant_id}", response_model=schemas.TenantResponse)
def get_tenant(tenant_id: int, db: Session = Depends(get_db)):
    tenant = db.query(models.Tenant).filter(models.Tenant.id == tenant_id).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return tenant

@router.put("/{tenant_id}", response_model=schemas.TenantResponse)
def update_tenant(tenant_id: int, payload: schemas.TenantUpdate, db: Session = Depends(get_db)):
    tenant = db.query(models.Tenant).filter(models.Tenant.id == tenant_id).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")

    for k, v in payload.dict(exclude_unset=True).items():
        setattr(tenant, k, v)

    db.commit()
    db.refresh(tenant)
    return tenant

@router.delete("/{tenant_id}")
def delete_tenant(tenant_id: int, db: Session = Depends(get_db)):
    tenant = db.query(models.Tenant).filter(models.Tenant.id == tenant_id).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    db.delete(tenant)
    db.commit()
    return {"detail": "Tenant deleted successfully"}
