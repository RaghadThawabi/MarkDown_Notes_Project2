from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from app.schemas.tags import TagOut


class NoteCreate(BaseModel):
    title: str
    content: Optional[str]
    tags: List[str] = []

class NoteUpdate(BaseModel):
    title: Optional[str]
    content: Optional[str]
    tags:List[str] = []

class NoteResponse(BaseModel):
    id: UUID
    title: str
    content: Optional[str]

    tags: List[TagOut]


    class Config:
        orm_mode = True
    owner_id: UUID
    is_deleted: bool