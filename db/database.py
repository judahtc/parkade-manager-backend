import os

from decouple import config
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = (
    "postgresql://{username}:{password}@{host}:{port}/{database}".format(
        username=config("RDS_USERNAME"),
        password=config("RDS_PASSWORD"),
        host=config("RDS_HOSTNAME"),
        port=config("RDS_PORT"),
        database=config("RDS_DB_NAME"),
    )
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(bind=engine)


RDS_DB_SCHEMA = config("RDS_DB_SCHEMA")
metadata = MetaData(schema=RDS_DB_SCHEMA)
Base = declarative_base(metadata=metadata)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
