from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from app.models.user  import Base

class Note(Base):
    __tablename__ = "notes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    content = Column(String, nullable=True)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    is_deleted = Column(Boolean, default=False)

    revisions = relationship(
        "NoteRevision",
        back_populates="note",
        cascade="all, delete"
    )#as I said in revisions table , to be able to have the notes versions and vise versa

    tags = relationship(
        "Tag",
        secondary="note_tags",
        back_populates="notes"
    )
    owner = relationship("User")
