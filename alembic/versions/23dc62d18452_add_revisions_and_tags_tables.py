"""Add revisions and tags tables

Revision ID: 23dc62d18452
Revises: 1db5afecce5a
Create Date: 2025-12-21 11:33:43.269923

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg


# revision identifiers, used by Alembic.
revision: str = '23dc62d18452'
down_revision: Union[str, Sequence[str], None] = '1db5afecce5a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    # Create Tag table
    op.create_table(
        'tags',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(), nullable=False, unique=True)
    )

    # Create NoteRevision table
    op.create_table(
        "note_revisions",
        sa.Column("id", pg.UUID(as_uuid=True), primary_key=True, default=sa.text("gen_random_uuid()")),
        sa.Column("note_id", pg.UUID(as_uuid=True), sa.ForeignKey("notes.id", ondelete="CASCADE"), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("content", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
    )

    # Create association table note_tags
    op.create_table(
        "note_tags",
        sa.Column("note_id", pg.UUID(as_uuid=True), sa.ForeignKey("notes.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("tag_id", sa.Integer, sa.ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
    )


def downgrade():
    # Drop tables in reverse order
    op.drop_table('note_tags')
    op.drop_table('note_revisions')
    op.drop_table('tags')