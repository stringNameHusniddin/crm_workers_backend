"""empty message

Revision ID: 53c9c195a45c
Revises: 28b20d917a9a
Create Date: 2023-08-15 09:09:13.863632

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '53c9c195a45c'
down_revision: Union[str, None] = '28b20d917a9a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'join_data')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('join_data', sa.INTEGER(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
