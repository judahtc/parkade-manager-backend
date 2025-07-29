from datetime import datetime, timedelta, timezone
from typing import Annotated
from decouple import config
import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel
import time


def create_access_token(data: dict):
    if not isinstance(data, dict):
        data = data.dict()
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config(
        "secret"), algorithm=config("algorithm"))
    return {"access_token": encoded_jwt}


def decodeJWT(token: str) -> dict:
    JWT_ALGORITHM = config("algorithm")
    JWT_SECRET = config("secret")

    try:
        decoded_token = jwt.decode(
            token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {"response": "token expired"}
