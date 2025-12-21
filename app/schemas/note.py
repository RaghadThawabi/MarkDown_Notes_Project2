from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class NoteCreate(BaseModel):
    title: str
    content: Optional[str]

class NoteUpdate(BaseModel):
    title: Optional[str]
    content: Optional[str]

class NoteResponse(BaseModel):
    id: UUID
    title: str
    content: Optional[str]
    owner_id: UUID
    is_deleted: bool

    class Configration:
        orm_mode = True
