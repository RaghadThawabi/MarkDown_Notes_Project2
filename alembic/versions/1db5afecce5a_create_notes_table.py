"""create notes table

Revision ID: 1db5afecce5a
Revises: 10506951739c
Create Date: 2025-12-21 10:08:16.950966

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg


# revision identifiers, used by Alembic.
revision: str = '1db5afecce5a'
down_revision: Union[str, Sequence[str], None] = '10506951739c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'notes',
        sa.Column('id', pg.UUID(as_uuid=True), primary_key=True, default=sa.text('gen_random_uuid()')),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('content', sa.String(), nullable=True),
        sa.Column('owner_id', pg.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('is_deleted', sa.Boolean(), nullable=False, server_default='false')
    )


def downgrade() -> None:
    op.drop_table('notes')
