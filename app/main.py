from fastapi import FastAPI
from app.routes import auth
from app.models.database import create_tables

app = FastAPI(title="IoT Data API", version="1.0")

create_tables()

app.include_router(auth.router)