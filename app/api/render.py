from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.core.database import get_db
from app.services.authorization_service import get_current_user
from app.services.markdown_service import MarkdownService
from app.models.user import User
from app.models.note import Note
from sqlalchemy.future import select

router = APIRouter(prefix="/notes", tags=["Rendering"])


@router.get(
    "/{note_id}/render",
    responses={
        200: {
            "description": "Successful Response",
            "content": {
                "text/html": {
                    "example": "<!DOCTYPE html><html><body><h1>Rendered Note</h1></body></html>"
                },
                "application/json": {
                    "example": {
                        "note_id": "550e8400-e29b-41d4-a716-446655440000",
                        "title": "My Note",
                        "html": "<h1>My Note</h1><p>Content here</p>",
                        "markdown": "# My Note\n\nContent here"
                    }
                }
            }
        },
        304: {
            "description": "Not Modified (Cached)"
        },
        404: {
            "description": "Note not found"
        }
    },
    summary="Render note as HTML or JSON",
    description="""
    Fetch sanitized HTML derived from a note's Markdown content.

    Features:
    - Content negotiation via Accept header (supports text/html and application/json)
    - ETag support for HTTP caching
    - If-None-Match header support for 304 Not Modified responses

    Accept header options:
    - text/html: Returns raw HTML content (default)
    - application/json: Returns JSON with html field
    - */*: Defaults to text/html
    """
)
async def render_note(
        note_id: UUID,
        request: Request,
        response: Response,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """
    Render a note's Markdown content as HTML or JSON.
    """
    # Fetch the note
    result = await db.execute(
        select(Note).where(
            Note.id == note_id,
            Note.owner_id == current_user.id,
            Note.is_deleted == False
        )
    )
    note = result.scalar_one_or_none()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    # Combine title and content for rendering
    markdown_content = f"# {note.title}\n\n{note.content or ''}"

    # Render to HTML and generate ETag
    html_content, etag = MarkdownService.render_with_etag(markdown_content)

    # Check If-None-Match header for caching
    if_none_match = request.headers.get("If-None-Match")
    if if_none_match and if_none_match == etag:
        # Content hasn't changed, return 304 Not Modified
        return Response(status_code=304, headers={"ETag": etag})

    # Set ETag and Cache-Control headers
    headers = {
        "ETag": etag,
        "Cache-Control": "private, max-age=3600"  # Cache for 1 hour
    }

    # Content negotiation based on Accept header
    accept_header = request.headers.get("Accept", "text/html")

    if "application/json" in accept_header:
        # Return JSON response
        return JSONResponse(
            content={
                "note_id": str(note_id),
                "title": note.title,
                "html": html_content,
                "markdown": markdown_content
            },
            headers=headers
        )
    else:
        # Default to HTML response
        # Wrap in a basic HTML document for better rendering
        full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{note.title}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
        }}
        code {{
            background-color: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }}
        pre {{
            background-color: #f4f4f4;
            padding: 10px;
            border-radius: 5px;
            overflow-x: auto;
        }}
        pre code {{
            background: none;
            padding: 0;
        }}
        blockquote {{
            border-left: 4px solid #ddd;
            padding-left: 16px;
            color: #666;
            margin: 16px 0;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 16px 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }}
        th {{
            background-color: #f4f4f4;
        }}
        img {{
            max-width: 100%;
            height: auto;
        }}
    </style>
</head>
<body>
    {html_content}
</body>
</html>"""

        return HTMLResponse(content=full_html, headers=headers)


@router.get("/{note_id}/render/raw", response_class=HTMLResponse)
async def render_note_raw(
        note_id: UUID,
        request: Request,
        response: Response,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """
    Get raw sanitized HTML without wrapper (useful for embedding).

    Returns only the rendered Markdown HTML without the document wrapper.
    """
    # Fetch the note
    result = await db.execute(
        select(Note).where(
            Note.id == note_id,
            Note.owner_id == current_user.id,
            Note.is_deleted == False
        )
    )
    note = result.scalar_one_or_none()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    # Combine title and content for rendering
    markdown_content = f"# {note.title}\n\n{note.content or ''}"

    # Render to HTML and generate ETag
    html_content, etag = MarkdownService.render_with_etag(markdown_content)

    # Check If-None-Match header for caching
    if_none_match = request.headers.get("If-None-Match")
    if if_none_match and if_none_match == etag:
        return Response(status_code=304, headers={"ETag": etag})

    # Set headers
    headers = {
        "ETag": etag,
        "Cache-Control": "private, max-age=3600"
    }

    return HTMLResponse(content=html_content, headers=headers)