from fastapi import FastAPI
from app.routes import auth, data, health, server
from app.models.database import create_tables
from app.models.database import engine, Base

app = FastAPI(title="IoT Data API", version="1.0")
create_tables()

app.include_router(auth.router)
app.include_router(data.router)
app.include_router(health.router)
app.include_router(server.router)