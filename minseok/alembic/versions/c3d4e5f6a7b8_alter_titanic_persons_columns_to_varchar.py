"""alter_titanic_persons_columns_to_varchar

Revision ID: c3d4e5f6a7b8
Revises: b2c3d4e5f6a7
Create Date: 2026-06-10 11:50:28.141505

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c3d4e5f6a7b8'
down_revision: Union[str, Sequence[str], None] = 'b2c3d4e5f6a7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("titanic_persons", "passenger_id", type_=sa.String(), existing_type=sa.Integer(), postgresql_using="passenger_id::varchar")
    op.alter_column("titanic_persons", "age",          type_=sa.String(), existing_type=sa.Float(),   postgresql_using="age::varchar")
    op.alter_column("titanic_persons", "sib_sp",       type_=sa.String(), existing_type=sa.Integer(), postgresql_using="sib_sp::varchar")
    op.alter_column("titanic_persons", "parch",        type_=sa.String(), existing_type=sa.Integer(), postgresql_using="parch::varchar")
    op.alter_column("titanic_persons", "survived",     type_=sa.String(), existing_type=sa.Integer(), postgresql_using="survived::varchar")


def downgrade() -> None:
    op.alter_column("titanic_persons", "passenger_id", type_=sa.Integer(), existing_type=sa.String(), postgresql_using="passenger_id::integer")
    op.alter_column("titanic_persons", "age",          type_=sa.Float(),   existing_type=sa.String(), postgresql_using="NULLIF(age, '')::float")
    op.alter_column("titanic_persons", "sib_sp",       type_=sa.Integer(), existing_type=sa.String(), postgresql_using="sib_sp::integer")
    op.alter_column("titanic_persons", "parch",        type_=sa.Integer(), existing_type=sa.String(), postgresql_using="parch::integer")
    op.alter_column("titanic_persons", "survived",     type_=sa.Integer(), existing_type=sa.String(), postgresql_using="survived::integer")
