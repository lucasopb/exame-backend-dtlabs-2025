from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.services.server_services import create_server
from app.schemas.server import ServerCreate, ServerResponse

router = APIRouter()

@router.post("/servers", response_model=ServerResponse)
def register_server(server: ServerCreate, db: Session = Depends(get_db)):
    db_server = create_server(db, server)
    return ServerResponse(
        server_ulid=db_server.server_ulid,
        name=db_server.name,
        is_online=db_server.is_online
    )