"""Adding rating column

Revision ID: 91f7541d7b79
Revises: 6cc18ffb98c5
Create Date: 2025-05-18 16:01:05.243828

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '91f7541d7b79'
down_revision: Union[str, None] = '6cc18ffb98c5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'posts',
        sa.Column('rating', sa.Float(), server_default=sa.text("0.0"), nullable=True)
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'rating')
    pass
