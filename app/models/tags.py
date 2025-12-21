from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.models.user import Base

note_tags = Table( #many-many table , to have each note has multi tags , and the tags belongs to multi notes
    "note_tags",
    Base.metadata,
    Column("note_id", ForeignKey("notes.id")),
    Column("tag_id", ForeignKey("tags.id")),
)


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    notes = relationship("Note", secondary=note_tags, back_populates="tags")
#secondary to say that I have relation many-many between tags and notes