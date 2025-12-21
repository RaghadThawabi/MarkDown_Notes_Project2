import uuid
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID  # native uuid for the postgresql

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.user import Base


class NoteRevision(Base):
    __tablename__ = "note_revisions"
    id = Column(
        UUID(as_uuid=True),  # Store as uuid object
        primary_key=True,
        default=uuid4,
        nullable=False
    )
    note_id = Column(UUID(as_uuid=True), ForeignKey("notes.id", ondelete="CASCADE"))
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    note = relationship("Note", back_populates="revisions")
    #back_populates = to have two sides relation , get the parent note from revisions
    #and get the revisions fron the note
