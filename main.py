from typing import Union
from api import vehicle,company,payment

from fastapi import FastAPI, HTTPException
import httpx

from models import models
from db.database import engine
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(
    title="Parkade Manager System",
    description="""
The Parkade Manager System is a secure and scalable platform for managing access to parking facilities. 
It supports verification and tracking of authorized vehicles, companies, visitors, and users across multiple tenants.

Core functionalities include:
- Vehicle registration and verification using license plate numbers
- Company onboarding and vehicle association
- Payment tracking for parking and related services
- Role-based access for admins, tenant managers, and security personnel
- Multi-tenant architecture to isolate and manage organizational data

The system enhances security, accountability, and operational efficiency for parkade facilities.
""",
    version="1.0.0",
)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
models.Base.metadata.create_all(bind=engine)
GITHUB_API_BASE_URL = "https://api.github.com"


@app.get("/health")
def read_root():
    return {"Hey": "I am working"}



app.include_router(vehicle.router)
app.include_router(company.router)
app.include_router(payment.router)

