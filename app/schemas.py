from typing import Optional
from pydantic import BaseModel

class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None

class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    class Config:
        orm_mode = True
