"""add deprecated field to spec table

Revision ID: daeb6373f743
Revises:
Create Date: 2022-06-14 13:53:44.632937

"""
import sqlalchemy as sa

from alembic import op


# revision identifiers, used by Alembic.
revision = 'daeb6373f743'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "spec", sa.Column("is_deprecated", sa.Boolean, nullable=True, default=False)
    )


def downgrade():
    op.drop_column("spec", "is_deprecated")
