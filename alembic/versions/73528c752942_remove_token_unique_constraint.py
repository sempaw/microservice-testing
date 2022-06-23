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
    op.drop_constraint(
        constraint_name="contract_token_key", table_name="contract", type_="unique"
    )
    op.drop_constraint(
        constraint_name="spec_token_key", table_name="spec", type_="unique"
    )


def downgrade():
    op.create_unique_constraint("contract_token_key", "contract", ["token"])
    op.create_unique_constraint("spec_token_key", "spec", ["token"])
