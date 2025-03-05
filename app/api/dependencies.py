from fastapi.security import OAuth2PasswordBearer
from app.core.jwt import verify_token  # Importando de jwt.py
from app.models.user import User
from app.models.database import Session, get_db
from fastapi import Depends, HTTPException
import logging

# Definindo o oauth2_scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Configuração do logger
logger = logging.getLogger(__name__)

def get_user_by_token(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        # Tente verificar o token
        payload = verify_token(token)
        
        # Se o token for válido, recupere o usuário
        user = db.query(User).filter(User.username == payload.get("sub")).first()
        if not user:
            logger.error(f"User with username {payload.get('sub')} not found.")
            raise HTTPException(
                status_code=401,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user
    except Exception as e:
        # Log do erro com mais detalhes
        logger.error(f"Error verifying token or fetching user: {str(e)}")
        raise HTTPException(
            status_code=401,
            detail="Invalid token or error fetching user",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_current_user(token: str = Depends(get_user_by_token)):
    if not token:
        logger.error("No token provided or token is invalid.")
        raise HTTPException(
            status_code=401,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token
