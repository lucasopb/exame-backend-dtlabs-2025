from fastapi import APIRouter, Depends, HTTPException
from app.models.database import get_db
from app.models.server import Server
from sqlalchemy.orm import Session
from app.api.dependencies import get_current_user  
from app.models.user import User  


router = APIRouter()

@router.get("/health/all")
def get_all_servers_health(db: Session = Depends(get_db)):
    servers = db.query(Server).all()

    return [
        {
            "server_ulid": server.server_ulid,
            "server_name": server.name,
            "status": server.is_online 
        }
        for server in servers
    ]

@router.get("/health/{server_ulid}")
def get_server_health(server_ulid: str, db: Session = Depends(get_db)):
    server = db.query(Server).filter(Server.server_ulid == server_ulid).first()

    if not server:
        raise HTTPException(status_code=404, detail="Server not found")

    return {
        "server_ulid": server.server_ulid,
        "server_name": server.name,
        "status": server.is_online  
    }