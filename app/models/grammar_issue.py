import uuid
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, ForeignKey, DateTime, Integer, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.user import Base


class GrammarIssue(Base):
    __tablename__ = "grammar_issues"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, nullable=False)
    revision_id = Column(UUID(as_uuid=True), ForeignKey("note_revisions.id", ondelete="CASCADE"), nullable=False)

    message = Column(Text, nullable=False)  #error
    short_message = Column(String, nullable=True)
    offset = Column(Integer, nullable=False)
    length = Column(Integer, nullable=False)

    context = Column(Text, nullable=True)

    replacements = Column(Text, nullable=True)  #  suggested fixes

    issue_type = Column(String, nullable=True)
    rule_id = Column(String, nullable=True)
    category = Column(String, nullable=True)

    is_applied = Column(Boolean, default=False)  #fixed or not

    created_at = Column(DateTime, default=datetime.utcnow)

    revision = relationship("NoteRevision", backref="grammar_issues")
