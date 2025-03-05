from pydantic import BaseModel

class ServerCreate(BaseModel):
    name: str

class ServerResponse(BaseModel):
    name: str
