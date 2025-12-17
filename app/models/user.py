from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID  # native uuid for the postgresql

from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True),  # Store as uuid object
        primary_key=True,
        default=uuid4,
        nullable=False
    )
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
