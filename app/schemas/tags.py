from pydantic import BaseModel
from uuid import UUID


class TagCreate(BaseModel):
    name: str


class TagOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
