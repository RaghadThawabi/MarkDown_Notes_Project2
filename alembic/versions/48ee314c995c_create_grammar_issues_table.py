"""create grammar_issues table

Revision ID: 48ee314c995c
Revises: 23dc62d18452
Create Date: 2025-12-21 18:55:18.609801

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision: str = '48ee314c995c'
down_revision: Union[str, Sequence[str], None] = '23dc62d18452'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Create grammar_issues table
    op.create_table(
        'grammar_issues',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('revision_id', UUID(as_uuid=True), sa.ForeignKey('note_revisions.id', ondelete='CASCADE'),
                  nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('short_message', sa.String(), nullable=True),
        sa.Column('offset', sa.Integer(), nullable=False),
        sa.Column('length', sa.Integer(), nullable=False),
        sa.Column('context', sa.Text(), nullable=True),
        sa.Column('replacements', sa.Text(), nullable=True),
        sa.Column('issue_type', sa.String(), nullable=True),
        sa.Column('rule_id', sa.String(), nullable=True),
        sa.Column('category', sa.String(), nullable=True),
        sa.Column('is_applied', sa.Boolean(), default=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    )

    # Create index on revision_id for faster queries
    op.create_index('ix_grammar_issues_revision_id', 'grammar_issues', ['revision_id'])


def downgrade():
    op.drop_index('ix_grammar_issues_revision_id', 'grammar_issues')
    op.drop_table('grammar_issues')