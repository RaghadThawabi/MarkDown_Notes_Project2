from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
from app.models.note import Note
from app.schemas.note import NoteCreate, NoteUpdate
from uuid import UUID

async def create_note(db: AsyncSession, note: NoteCreate, owner_id: UUID):
    new_note = Note(title=note.title, content=note.content, owner_id=owner_id)
    db.add(new_note)
    await db.commit()
    await db.refresh(new_note)
    return new_note

async def get_notes(db: AsyncSession, owner_id: UUID):
    result = await db.execute(
        select(Note).where(Note.owner_id == owner_id, Note.is_deleted == False)
    )
    return result.scalars().all()

async def get_note_by_id(db: AsyncSession, note_id: UUID, owner_id: UUID):
    result = await db.execute(
        select(Note).where(Note.id == note_id, Note.owner_id == owner_id, Note.is_deleted == False)
    )
    return result.scalar_one_or_none()

async def update_note(db: AsyncSession, note_id: UUID, owner_id: UUID, note_data: NoteUpdate):
    result = await db.execute(
        select(Note).where(Note.id == note_id, Note.owner_id == owner_id, Note.is_deleted == False)
    )
    note = result.scalar_one_or_none()
    if note:
        if note_data.title is not None:
            note.title = note_data.title
        if note_data.content is not None:
            note.content = note_data.content
        await db.commit()
        await db.refresh(note)
    return note

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
