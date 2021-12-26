"""add forign key to post table

Revision ID: 0ce4e1f4999d
Revises: fa56402c7e0a
Create Date: 2021-12-25 19:25:18.194858

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import null, table


# revision identifiers, used by Alembic.
revision = '0ce4e1f4999d'
down_revision = 'fa56402c7e0a'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table='posts', referent_table='users', local_cols=[
                          'owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade():
    op.drop_constraint('posts_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
