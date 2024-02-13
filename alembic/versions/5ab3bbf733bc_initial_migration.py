"""Initial migration

Revision ID: 5ab3bbf733bc
Revises: 884e99692a4e
Create Date: 2024-02-12 00:25:49.775238

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5ab3bbf733bc'
down_revision: Union[str, None] = '884e99692a4e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
