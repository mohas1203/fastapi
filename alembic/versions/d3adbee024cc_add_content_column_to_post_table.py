"""add content column to post table

Revision ID: d3adbee024cc
Revises: 69abce35b41b
Create Date: 2021-12-25 19:12:25.845143

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd3adbee024cc'
down_revision = '69abce35b41b'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
