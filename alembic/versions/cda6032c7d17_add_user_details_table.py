"""add user_details table

Revision ID: cda6032c7d17
Revises: f9c2bcdcb7e0
Create Date: 2026-06-01 17:36:52.731468

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cda6032c7d17'
down_revision = 'f9c2bcdcb7e0'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('user_details', sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False, unique=True),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
    sa.PrimaryKeyConstraint('id'))
    pass


def downgrade():
    op.drop_table('user_details')
    pass
