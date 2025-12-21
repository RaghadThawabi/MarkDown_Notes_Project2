from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.models.note import Note
from app.services.note_service import create_note, get_notes, get_note_by_id, update_note, soft_delete_note
from app.schemas.note import NoteCreate, NoteUpdate, NoteResponse
from app.services.authorization_service import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.models.note_revision import NoteRevision
from app.models.tags import Tag
from app.schemas.revisions import RevisionOut
from sqlalchemy.orm import selectinload

router = APIRouter(prefix="/notes", tags=["Notes"])


async def update_note_with_revision(
        db: AsyncSession,
        note_id: UUID,
        user_id: UUID,
        note_data: NoteUpdate
):
    # Step 1: Fetch the note with tags eagerly loaded
    result = await db.execute(
        select(Note)
        .options(selectinload(Note.tags))
        .where(
            Note.id == note_id,
            Note.owner_id == user_id,
            Note.is_deleted == False
        )
    )

    note = result.scalar_one_or_none()
    if not note:
        return None

    old_title = note.title
    old_content = note.content if note.content else ""

    revision = NoteRevision(
        note_id=note.id,
        title=old_title,
        content=old_content
    )
    db.add(revision)

    if note_data.title is not None:
        note.title = note_data.title
    if note_data.content is not None:
        note.content = note_data.content

    if note_data.tags:
        tags_list = []
        for tag_name in note_data.tags:
            tag_result = await db.execute(select(Tag).where(Tag.name == tag_name))
            tag = tag_result.scalar_one_or_none()
            if not tag:
                tag = Tag(name=tag_name)
                db.add(tag)
                await db.flush()  # Flush to get the tag ID
            tags_list.append(tag)
        note.tags = tags_list

    await db.commit()

    await db.refresh(note, attribute_names=["tags"])

    return note


@router.post("/", response_model=NoteResponse, status_code=201)
async def create_new_note(note: NoteCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await create_note(db, note, current_user.id)

@router.get("/", response_model=list[NoteResponse])
async def list_notes(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await get_notes(db, current_user.id)

@router.get("/{note_id}", response_model=NoteResponse)
async def get_single_note(note_id: UUID, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    note = await get_note_by_id(db, note_id, current_user.id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@router.put("/{note_id}", response_model=NoteResponse)
async def update_existing_note(
    note_id: UUID,
    note_data: NoteUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    note = await update_note_with_revision(db, note_id, current_user.id, note_data)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@router.delete("/{note_id}", response_model=NoteResponse)
async def delete_note(note_id: UUID, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    note = await soft_delete_note(db, note_id, current_user.id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@router.get("/{note_id}/revisions", response_model=list[RevisionOut])
async def get_revisions(
    note_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(NoteRevision)
        .join(Note)
        .where(Note.id == note_id, Note.owner_id == current_user.id)
    )
    # the join is to ensure the note belong to the logged in user

    return result.scalars().all()

@router.post("/{note_id}/revisions/{revision_id}/restore")
async def restore_revision(
    note_id: UUID,
    revision_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Note, NoteRevision)
        .join(NoteRevision)
        .where(
            Note.id == note_id,
            Note.owner_id == current_user.id,
            NoteRevision.id == revision_id
        )
    )#rewtore the note ane the version i need

    note, revision = result.first() or (None, None)

    if not note:
        raise HTTPException(status_code=404, detail="Revision not found")
#this copy the content of the version to the current
    note.title = revision.title
    note.content = revision.content

    await db.commit()

    return {"message": "Revision restored successfully"}


@router.get("/tags/{tag_name}", response_model=list[NoteResponse])
async def get_notes_by_tag(
        tag_name: str,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    tag_result = await db.execute(select(Tag).where(Tag.name == tag_name))
    tag = tag_result.scalar_one_or_none()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    # Reuse working function and filter in Python
    all_notes = await get_notes(db, current_user.id)
    filtered_notes = [note for note in all_notes if any(t.name == tag_name for t in note.tags)]

    return filtered_notes
