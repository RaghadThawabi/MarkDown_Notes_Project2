from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
import json

from app.core.database import get_db
from app.services.authorization_service import get_current_user
from app.services.grammar_service import GrammarService
from app.schemas.grammar import (
    GrammarCheckResponse,
    GrammarIssueOut,
    ApplyFixesRequest,
    ApplyFixesResponse
)
from app.models.user import User
from app.models.note import Note
from app.models.note_revision import NoteRevision
from sqlalchemy.future import select

router = APIRouter(prefix="/notes", tags=["Grammar Checking"])


@router.post("/{note_id}/revisions/{revision_id}/grammar-check", response_model=GrammarCheckResponse)
async def check_grammar(
        note_id: UUID,
        revision_id: UUID,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):

    # Verify user owns the note
    result = await db.execute(
        select(Note)
        .join(NoteRevision)
        .where(
            Note.id == note_id,
            Note.owner_id == current_user.id,
            NoteRevision.id == revision_id
        )
    )
    note = result.scalar_one_or_none()

    if not note:
        raise HTTPException(
            status_code=404,
            detail="Note or revision not found"
        )

    # Run grammar check
    try:
        issues = await GrammarService.check_revision(db, revision_id)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Grammar check failed: {str(e)}"
        )

    # Convert to response format
    issues_out = []
    for issue in issues:
        replacements = json.loads(issue.replacements) if issue.replacements else []
        issues_out.append(
            GrammarIssueOut(
                id=issue.id,
                revision_id=issue.revision_id,
                message=issue.message,
                short_message=issue.short_message,
                offset=issue.offset,
                length=issue.length,
                context=issue.context,
                replacements=replacements,
                issue_type=issue.issue_type,
                rule_id=issue.rule_id,
                category=issue.category,
                is_applied=issue.is_applied,
                created_at=issue.created_at
            )
        )

    return GrammarCheckResponse(
        revision_id=revision_id,
        total_issues=len(issues_out),
        issues=issues_out
    )


@router.get("/{note_id}/revisions/{revision_id}/grammar-issues", response_model=GrammarCheckResponse)
async def get_grammar_issues(
        note_id: UUID,
        revision_id: UUID,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):

    # Verify user owns the note
    result = await db.execute(
        select(Note)
        .join(NoteRevision)
        .where(
            Note.id == note_id,
            Note.owner_id == current_user.id,
            NoteRevision.id == revision_id
        )
    )
    note = result.scalar_one_or_none()

    if not note:
        raise HTTPException(
            status_code=404,
            detail="Note or revision not found"
        )

    # Get stored issues
    issues = await GrammarService.get_issues(db, revision_id)

    # Convert to response format
    issues_out = []
    for issue in issues:
        replacements = json.loads(issue.replacements) if issue.replacements else []
        issues_out.append(
            GrammarIssueOut(
                id=issue.id,
                revision_id=issue.revision_id,
                message=issue.message,
                short_message=issue.short_message,
                offset=issue.offset,
                length=issue.length,
                context=issue.context,
                replacements=replacements,
                issue_type=issue.issue_type,
                rule_id=issue.rule_id,
                category=issue.category,
                is_applied=issue.is_applied,
                created_at=issue.created_at
            )
        )

    return GrammarCheckResponse(
        revision_id=revision_id,
        total_issues=len(issues_out),
        issues=issues_out
    )


@router.post("/{note_id}/revisions/{revision_id}/apply-fixes", response_model=ApplyFixesResponse)
async def apply_grammar_fixes(
        note_id: UUID,
        revision_id: UUID,
        request: ApplyFixesRequest,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):

    # Verify user owns the note
    result = await db.execute(
        select(Note)
        .join(NoteRevision)
        .where(
            Note.id == note_id,
            Note.owner_id == current_user.id,
            NoteRevision.id == revision_id
        )
    )
    note = result.scalar_one_or_none()

    if not note:
        raise HTTPException(
            status_code=404,
            detail="Note or revision not found"
        )

    # Apply fixes
    try:
        corrected_content = await GrammarService.apply_fixes(
            db,
            revision_id,
            request.issue_ids
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to apply fixes: {str(e)}"
        )

    return ApplyFixesResponse(
        applied_count=len(request.issue_ids),
        new_content=corrected_content,
        message=f"Applied {len(request.issue_ids)} grammar fixes. Use the update endpoint to save changes."
    )
