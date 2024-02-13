"""Initial migration

Revision ID: 884e99692a4e
Revises: 185f2b241e08
Create Date: 2024-02-12 00:20:41.197138

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '884e99692a4e'
down_revision: Union[str, None] = '185f2b241e08'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
