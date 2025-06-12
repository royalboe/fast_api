"""adding new column (update_at)

Revision ID: 01869217abca
Revises: 0c9abdd629c4
Create Date: 2025-05-18 15:33:32.679213

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '01869217abca'
down_revision: Union[str, None] = '0c9abdd629c4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'posts', 
        sa.Column(
            'updated_at', 
            sa.DateTime(timezone=True), 
            server_default=sa.text("CURRENT_TIMESTAMP"), 
            nullable=False
            )
        )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'updated_at')
    pass
