from passlib.context import CryptContext
from app.core.jwt import create_access_token  # Importa de jwt.py
from app.models.user import User
from app.models.database import Session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)

