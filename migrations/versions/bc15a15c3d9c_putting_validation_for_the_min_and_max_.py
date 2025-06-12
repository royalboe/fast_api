"""putting validation for the min and max number of characters for title and content

Revision ID: bc15a15c3d9c
Revises: 49f4602e7ad8
Create Date: 2025-06-10 17:33:25.382931

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'bc15a15c3d9c'
down_revision: Union[str, None] = '49f4602e7ad8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add CHECK constraints
    op.execute("ALTER TABLE posts ADD CONSTRAINT title_length CHECK (char_length(title) BETWEEN 5 AND 100)")
    op.execute("ALTER TABLE posts ADD CONSTRAINT content_length CHECK (char_length(content) >= 5)")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("ALTER TABLE posts DROP CONSTRAINT title_length")
    op.execute("ALTER TABLE posts DROP CONSTRAINT content_length")
