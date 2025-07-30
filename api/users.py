from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from db.database import get_db
from models import models
from schemas import schemas

router = APIRouter(prefix="/users", tags=["users"])

# --- simple password hasher (replace with passlib in production) ---
import hashlib
def get_password_hash(raw: str) -> str:
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()
# -------------------------------------------------------------------

@router.post("", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    # Validate tenant exists
    tenant = db.query(models.Tenant).filter(models.Tenant.id == payload.tenant_id).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")

    # Unique checks
    if db.query(models.User).filter(models.User.username == payload.username).first():
        raise HTTPException(status_code=400, detail="Username already taken")
    if db.query(models.User).filter(models.User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    user = models.User(
        username=payload.username,
        full_name=payload.full_name,
        email=payload.email,
        role=payload.role,
        hashed_password=get_password_hash(payload.password),
        tenant_id=payload.tenant_id,
        is_active=True,
        created_at=datetime.utcnow(),
        last_login=None
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get("", response_model=List[schemas.UserResponse])
def list_users(
    tenant_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    q = db.query(models.User)
    if tenant_id is not None:
        q = q.filter(models.User.tenant_id == tenant_id)
    return q.offset(skip).limit(limit).all()

@router.get("/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=schemas.UserResponse)
def update_user(user_id: int, payload: schemas.UserUpdate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Optional uniqueness checks if username/email are being changed
    data = payload.dict(exclude_unset=True)

    new_email = data.get("email")
    if new_email and new_email != user.email:
        if db.query(models.User).filter(models.User.email == new_email).first():
            raise HTTPException(status_code=400, detail="Email already registered")

    # Apply changes
    for k, v in data.items():
        setattr(user, k, v)

    db.commit()
    db.refresh(user)
    return user

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"detail": "User deleted successfully"}

# Activate / Deactivate user
@router.put("/{user_id}/activate", response_model=schemas.UserResponse)
def activate_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_active = True
    db.commit()
    db.refresh(user)
    return user

@router.put("/{user_id}/deactivate", response_model=schemas.UserResponse)
def deactivate_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_active = False
    db.commit()
    db.refresh(user)
    return user

# Update last_login (call this from your auth flow)
@router.put("/{user_id}/last-login", response_model=schemas.UserResponse)
def set_last_login(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.last_login = datetime.utcnow()
    db.commit()
    db.refresh(user)
    return user
