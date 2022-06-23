"""move from pickle to json type

Revision ID: a146bd4ff65b
Revises:
Create Date: 2022-06-19 12:51:05.541052

"""
import sqlalchemy as sa

from alembic import op


# revision identifiers, used by Alembic.
revision = "a146bd4ff65b"
down_revision = None
branch_labels = None
depends_on = None


async def upgrade():
    op.alter_column("contract", "data", existing_type=sa.JSON)
    op.alter_column("spec", "data", existing_type=sa.JSON)


async def downgrade():
    op.alter_column("contract", "data", existing_type=sa.PickleType)
    op.alter_column("spec", "data", existing_type=sa.PickleType)
