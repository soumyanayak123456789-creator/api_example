"""add foreign key to posts table

Revision ID: 4710c14a679b
Revises: cda6032c7d17
Create Date: 2026-06-01 17:45:27.349033

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4710c14a679b'
down_revision = 'cda6032c7d17'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key('fk_posts_user_details_id', 'posts', 'user_details', ['user_id'], ['id'], ondelete='CASCADE')
    pass


def downgrade():
    op.drop_constraint('fk_posts_user_details_id', 'posts', type_='foreignkey')
    op.drop_column('posts', 'user_id')
    pass
