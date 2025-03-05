from sqlalchemy import Column, String, Boolean
from app.models.database import Base
import ulid

class Server(Base):
    __tablename__ = "servers"

    server_ulid = Column(String, primary_key=True, index=True, default=lambda: str(ulid.new()))  # Alterei para 'server_ulid'
    name = Column(String, nullable=False)
    is_online = Column(Boolean, default=False)