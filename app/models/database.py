from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from fastapi import Depends
from sqlalchemy.orm import Session

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/iot")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_session_local():
    yield SessionLocal()

Base = declarative_base()

def create_tables():
    from app.models.user import User
    from app.models.sensor import SensorData
    Base.metadata.create_all(bind=engine)

def get_db(db: Session = Depends(get_session_local)):
    try:
        yield db
    finally:
        db.close()
