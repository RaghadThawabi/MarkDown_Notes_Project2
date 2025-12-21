import markdown
import bleach
import hashlib
from typing import Tuple


class MarkdownService:
    """Service for rendering Markdown to sanitized HTML"""

    ALLOWED_TAGS = [
        'p', 'br', 'strong', 'em', 'u', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
        'blockquote', 'code', 'pre', 'hr', 'ul', 'ol', 'li', 'a', 'img',
        'table', 'thead', 'tbody', 'tr', 'th', 'td', 'div', 'span', 'del', 'ins'
    ]

    ALLOWED_ATTRIBUTES = {
        'a': ['href', 'title', 'target', 'rel'],
        'img': ['src', 'alt', 'title', 'width', 'height'],
        'code': ['class'],
        'pre': ['class'],
        'div': ['class'],
        'span': ['class'],
    }

    MARKDOWN_EXTENSIONS = [
        'extra',  # Tables, fenced code blocks, etc.
        'codehilite',  # Syntax highlighting
        'toc',  # Table of contents
        'nl2br',  # Newline to <br>
        'sane_lists',  # Better list handling
    ]

    @staticmethod
    def render_to_html(markdown_text: str) -> str:

        # Convert Markdown to HTML
        html = markdown.markdown(
            markdown_text,
            extensions=MarkdownService.MARKDOWN_EXTENSIONS,
            output_format='html5'
        )

        sanitized_html = bleach.clean(
            html,
            tags=MarkdownService.ALLOWED_TAGS,
            attributes=MarkdownService.ALLOWED_ATTRIBUTES,
            strip=True
        )

        return sanitized_html

    @staticmethod
    def generate_etag(content: str) -> str:

        content_hash = hashlib.md5(content.encode('utf-8')).hexdigest()
        return f'"{content_hash}"'

    @staticmethod
    def render_with_etag(markdown_text: str) -> Tuple[str, str]:

        html = MarkdownService.render_to_html(markdown_text)
        etag = MarkdownService.generate_etag(html)
        return html, etag
