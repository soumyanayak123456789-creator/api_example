"""add content column to posts table

Revision ID: f9c2bcdcb7e0
Revises: b835abf4287f
Create Date: 2026-06-01 16:13:03.574079

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f9c2bcdcb7e0'
down_revision = 'b835abf4287f'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
