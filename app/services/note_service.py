from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
from sqlalchemy.orm import selectinload

from app.models.note import Note
from app.models.tags import Tag
from app.schemas.note import NoteCreate, NoteUpdate, NoteResponse
from uuid import UUID

from app.schemas.tags import TagOut


async def create_note(db: AsyncSession, note_data, owner_id):
    # Create the note
    new_note = Note(
        title=note_data.title,
        content=note_data.content,
        owner_id=owner_id
    )

    # Handle tags
    tags_list = []
    for tag_name in note_data.tags:
        result = await db.execute(select(Tag).where(Tag.name == tag_name))
        tag = result.scalar_one_or_none()
        if not tag:
            tag = Tag(name=tag_name)
            db.add(tag)
        tags_list.append(tag)

    new_note.tags = tags_list
    db.add(new_note)
    await db.commit()
    await db.refresh(new_note)  # reload the note with tags

    # Make sure tags are loaded properly
    await db.refresh(new_note, attribute_names=["tags"])

    return new_note

async def get_notes(db: AsyncSession, owner_id: UUID):
    result = await db.execute(
        select(Note)
        .options(selectinload(Note.tags))  # <-- load tags with the note
        .where(Note.owner_id == owner_id, Note.is_deleted == False)
    )
    notes = result.scalars().all()
    return notes

async def get_note_by_id(db: AsyncSession, note_id: UUID, owner_id: UUID):
    result = await db.execute(
        select(Note).
        options(selectinload(Note.tags))  # <-- load tags with the note
        .where(Note.id == note_id, Note.owner_id == owner_id, Note.is_deleted == False)
    )
    return result.scalar_one_or_none()
async def update_note(db: AsyncSession, note_id: UUID, owner_id: UUID, note_data: NoteUpdate) -> NoteResponse:
    # Fetch the note
    result = await db.execute(
        select(Note)
        .options(selectinload(Note.tags))
        .where(
            Note.id == note_id,
            Note.owner_id == owner_id,
            Note.is_deleted == False
        )
    )
    note = result.scalar_one_or_none()
    if not note:
        return None  # you can handle 404 in the router

    # Update note fields
    if note_data.title is not None:
        note.title = note_data.title
    if note_data.content is not None:
        note.content = note_data.content

    await db.commit()
    await db.refresh(note)

    # Convert tags to Pydantic
    tags_out = [TagOut(id=tag.id, name=tag.name) for tag in note.tags]

    # Return Pydantic response
    return NoteResponse(
        id=note.id,
        owner_id=note.owner_id,
        title=note.title,
        content=note.content,
        is_deleted=note.is_deleted,

        tags=tags_out
    )


async def soft_delete_note(db: AsyncSession, note_id: UUID, owner_id: UUID):
    result = await db.execute(
        select(Note).where(Note.id == note_id, Note.owner_id == owner_id)
    )
    note = result.scalar_one_or_none()
    if note:
        note.is_deleted = True
        await db.commit()
        await db.refresh(note)
    return note
