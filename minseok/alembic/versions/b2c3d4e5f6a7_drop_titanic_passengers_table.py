"""drop_titanic_passengers_table

Revision ID: b2c3d4e5f6a7
Revises: a1b2c3d4e5f6
Create Date: 2026-06-04 00:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "b2c3d4e5f6a7"
down_revision: Union[str, Sequence[str], None] = "a1b2c3d4e5f6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_table("titanic_passengers")


def downgrade() -> None:
    op.create_table(
        "titanic_passengers",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("passenger_id", sa.Integer(), nullable=True),
        sa.Column("survived", sa.Integer(), nullable=True),
        sa.Column("pclass", sa.Integer(), nullable=True),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("sex", sa.String(), nullable=True),
        sa.Column("age", sa.Float(), nullable=True),
        sa.Column("sib_sp", sa.Integer(), nullable=True),
        sa.Column("parch", sa.Integer(), nullable=True),
        sa.Column("ticket", sa.String(), nullable=True),
        sa.Column("fare", sa.Float(), nullable=True),
        sa.Column("cabin", sa.String(), nullable=True),
        sa.Column("boat", sa.String(), nullable=True),
        sa.Column("embarked", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
