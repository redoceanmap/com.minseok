"""create_titanic_passengers_table

Revision ID: f1e2d3c4b5a6
Revises: d33b44e16399
Create Date: 2026-05-27 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'f1e2d3c4b5a6'
down_revision: Union[str, Sequence[str], None] = 'd33b44e16399'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'titanic_passengers',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('passenger_id', sa.Integer(), nullable=True),
        sa.Column('survived', sa.Integer(), nullable=True),
        sa.Column('pclass', sa.Integer(), nullable=True),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('sex', sa.String(), nullable=True),
        sa.Column('age', sa.Float(), nullable=True),
        sa.Column('sib_sp', sa.Integer(), nullable=True),
        sa.Column('parch', sa.Integer(), nullable=True),
        sa.Column('ticket', sa.String(), nullable=True),
        sa.Column('fare', sa.Float(), nullable=True),
        sa.Column('cabin', sa.String(), nullable=True),
        sa.Column('boat', sa.String(), nullable=True),
        sa.Column('embarked', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade() -> None:
    op.drop_table('titanic_passengers')
