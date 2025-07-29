from typing import Union
from api import patients, visitors, admins, hospital, security

from fastapi import FastAPI, HTTPException
import httpx

from models import models
from db.database import engine
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(title="Hospital Patient Visit Manager", description="The Hospital Security Application is a system designed to verify and manage authorized visitors for patients. The system will be run by Admins and Security personnel. Security will verify the visitor’s identity using their National ID and check against the patient's pre-authorized visitor list.", version="1.0.0",)
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


@app.get("/{username}")
async def get_user_gists(username: str):

    url = f"{GITHUB_API_BASE_URL}/users/{username}/gists"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
        if response.status_code == 200:
            gists = response.json()
            # Extract relevant data from each gist
            return [
                {
                    "id": gist["id"],
                    "description": gist.get("description", "No description"),
                    "url": gist["html_url"],
                }
                for gist in gists
            ]
        elif response.status_code == 404:
            raise HTTPException(status_code=404, detail="User not found")
        else:
            raise HTTPException(
                status_code=response.status_code, detail=response.json())
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=500, detail=f"Error connecting to GitHub API: {exc}")

app.include_router(security.router)
app.include_router(hospital.router)
app.include_router(admins.router)
app.include_router(patients.router)
app.include_router(visitors.router)
