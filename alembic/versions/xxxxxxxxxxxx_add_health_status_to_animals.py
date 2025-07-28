"""add health_status to animals

Revision ID: xxxxxxxxxxxx
Revises: 
Create Date: 2025-07-28

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'xxxxxxxxxxxx'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('animals', sa.Column('health_status', sa.String(), nullable=True))

def downgrade():
    op.drop_column('animals', 'health_status')