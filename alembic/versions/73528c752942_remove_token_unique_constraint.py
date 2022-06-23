"""remove token unique constraint

Revision ID: 73528c752942
Revises: a146bd4ff65b
Create Date: 2022-06-23 15:34:26.458525

"""

from alembic import op


# revision identifiers, used by Alembic.
revision = "73528c752942"
down_revision = "a146bd4ff65b"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column("contract", "token", unique=False)
    op.alter_column("spec", "token", unique=False)
    op.alter_column("user", "token", unique=False)


def downgrade():
    op.alter_column("contract", "token", unique=True)
    op.alter_column("spec", "token", unique=True)
    op.alter_column("user", "token", unique=True)
