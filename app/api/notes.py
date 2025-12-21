from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.services.note_service import create_note, get_notes, get_note_by_id, update_note, soft_delete_note
from app.schemas.note import NoteCreate, NoteUpdate, NoteResponse
from app.services.authorization_service import get_current_user
from app.core.database import get_db
from app.models.user import User

router = APIRouter(prefix="/notes", tags=["Notes"])

@router.post("/", response_model=NoteResponse, status_code=201)
async def create_new_note(note: NoteCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await create_note(db, note, current_user.id)

@router.get("/", response_model=list[NoteResponse])
async def list_notes(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await get_notes(db, current_user.id)

@router.get("/{note_id}", response_model=NoteResponse)
async def get_single_note(note_id: UUID, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    note = await get_note_by_id(db, note_id, current_user.id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@router.put("/{note_id}", response_model=NoteResponse)
async def update_existing_note(note_id: UUID, note_data: NoteUpdate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    note = await update_note(db, note_id, current_user.id, note_data)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found or no changes")
    return note

@router.delete("/{note_id}", response_model=NoteResponse)
async def delete_note(note_id: UUID, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    note = await soft_delete_note(db, note_id, current_user.id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note
