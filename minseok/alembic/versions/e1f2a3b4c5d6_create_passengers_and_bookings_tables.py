"""create_passengers_and_bookings_tables

Revision ID: e1f2a3b4c5d6
Revises: c3d4e5f6a7b8
Create Date: 2026-06-10

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'e1f2a3b4c5d6'
down_revision: Union[str, Sequence[str], None] = 'c3d4e5f6a7b8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'passengers',
        sa.Column('passenger_id', sa.String(), primary_key=True, nullable=True),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('gender', sa.String(), nullable=True),
        sa.Column('age', sa.String(), nullable=True),
        sa.Column('sib_sp', sa.String(), nullable=True),
        sa.Column('parch', sa.String(), nullable=True),
        sa.Column('survived', sa.String(), nullable=True),
    )
    op.create_table(
        'bookings',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('passenger_id', sa.String(), sa.ForeignKey('passengers.passenger_id'), nullable=True),
        sa.Column('pclass', sa.String(), nullable=True),
        sa.Column('ticket', sa.String(), nullable=True),
        sa.Column('fare', sa.String(), nullable=True),
        sa.Column('cabin', sa.String(), nullable=True),
        sa.Column('embarked', sa.String(), nullable=True),
    )


def downgrade() -> None:
    op.drop_table('bookings')
    op.drop_table('passengers')
