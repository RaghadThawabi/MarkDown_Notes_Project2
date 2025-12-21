from uuid import UUID

from pydantic import BaseModel
from datetime import datetime


class RevisionOut(BaseModel):
    id: UUID
    note_id: UUID
    title: str
    content: str
    created_at: datetime

    class Config:
        orm_mode = True
