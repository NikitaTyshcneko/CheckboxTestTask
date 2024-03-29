"""update models

Revision ID: 608aa1300463
Revises: ea5a45d59539
Create Date: 2024-02-13 18:51:20.688389

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '608aa1300463'
down_revision: Union[str, None] = 'ea5a45d59539'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('receipts', 'products',
               existing_type=postgresql.JSON(astext_type=sa.Text()),
               type_=sa.String(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('receipts', 'products',
               existing_type=sa.String(),
               type_=postgresql.JSON(astext_type=sa.Text()),
               nullable=True)
    # ### end Alembic commands ###
