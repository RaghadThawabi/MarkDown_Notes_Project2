import httpx
import json
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID

from app.models.grammar_issue import GrammarIssue
from app.models.note_revision import NoteRevision


class GrammarService:

    LANGUAGETOOL_API = "https://api.languagetool.org/v2/check"

    @staticmethod
    async def check_revision(db: AsyncSession, revision_id: UUID) -> List[GrammarIssue]:

        # Fetch the revision
        result = await db.execute(
            select(NoteRevision).where(NoteRevision.id == revision_id)
        )
        revision = result.scalar_one_or_none()

        if not revision:
            return []

        # Combine title and content for checking
        text_to_check = f"{revision.title}\n\n{revision.content}"

        # Clear existing issues for this revision
        await db.execute(
            select(GrammarIssue).where(GrammarIssue.revision_id == revision_id)
        )
        existing_issues = (await db.execute(
            select(GrammarIssue).where(GrammarIssue.revision_id == revision_id)
        )).scalars().all()

        for issue in existing_issues:
            await db.delete(issue)

        # Call LanguageTool API
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                GrammarService.LANGUAGETOOL_API,
                data={
                    "text": text_to_check,
                    "language": "en-US",
                }
            )

            if response.status_code != 200:
                raise Exception(f"LanguageTool API error: {response.status_code}")

            data = response.json()

        # Store issues in database
        grammar_issues = []
        for match in data.get("matches", []):
            # Extract replacements
            replacements = [r["value"] for r in match.get("replacements", [])[:5]]  # Limit to 5 suggestions

            grammar_issue = GrammarIssue(
                revision_id=revision_id,
                message=match.get("message", ""),
                short_message=match.get("shortMessage"),
                offset=match.get("offset", 0),
                length=match.get("length", 0),
                context=match.get("context", {}).get("text"),
                replacements=json.dumps(replacements),  # Store as JSON string
                issue_type=match.get("rule", {}).get("issueType"),
                rule_id=match.get("rule", {}).get("id"),
                category=match.get("rule", {}).get("category", {}).get("name"),
                is_applied=False
            )

            db.add(grammar_issue)
            grammar_issues.append(grammar_issue)

        await db.commit()

        # Refresh to get IDs
        for issue in grammar_issues:
            await db.refresh(issue)

        return grammar_issues

    @staticmethod
    async def get_issues(db: AsyncSession, revision_id: UUID) -> List[GrammarIssue]:
        """Get all grammar issues for a revision"""
        result = await db.execute(
            select(GrammarIssue)
            .where(GrammarIssue.revision_id == revision_id)
            .order_by(GrammarIssue.offset)
        )
        return result.scalars().all()

    @staticmethod
    async def apply_fixes(
            db: AsyncSession,
            revision_id: UUID,
            issue_ids: List[UUID]
    ) -> str:

        # Fetch revision
        result = await db.execute(
            select(NoteRevision).where(NoteRevision.id == revision_id)
        )
        revision = result.scalar_one_or_none()

        if not revision:
            raise ValueError("Revision not found")

        # Fetch issues to apply
        result = await db.execute(
            select(GrammarIssue)
            .where(
                GrammarIssue.revision_id == revision_id,
                GrammarIssue.id.in_(issue_ids)
            )
            .order_by(GrammarIssue.offset.desc())  # Apply from end to start
        )
        issues = result.scalars().all()

        # Combine title and content
        content = f"{revision.title}\n\n{revision.content}"

        # Apply fixes from end to start (to preserve offsets)
        applied_count = 0
        for issue in issues:
            replacements = json.loads(issue.replacements) if issue.replacements else []

            if replacements:
                # Use the first suggestion
                replacement = replacements[0]

                # Apply the fix
                start = issue.offset
                end = issue.offset + issue.length
                content = content[:start] + replacement + content[end:]

                # Mark as applied
                issue.is_applied = True
                applied_count += 1

        await db.commit()

        return content