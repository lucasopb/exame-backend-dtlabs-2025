from sqlalchemy import Column, Integer, String
from app.models.database import Base
import ulid

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True, default=lambda: str(ulid.new()))
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
