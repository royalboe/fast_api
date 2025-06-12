"""adding the foreign key constraint for post table  with users table

Revision ID: 1687947851bd
Revises: 91f7541d7b79
Create Date: 2025-05-18 16:06:59.811945

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1687947851bd'
down_revision: Union[str, None] = '91f7541d7b79'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'posts',
        sa.Column('author_id', sa.Integer(), nullable=False)
    )
    op.create_foreign_key(
        'posts_users_fk',
        source_table='posts',
        referent_table='users',
        local_cols=['author_id'],
        remote_cols=['id'],
        ondelete='CASCADE'
    )
    op.create_index(
        'title',
        'posts',
        ['title'],
        unique=True
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('posts_users_fk', 'posts')
    op.drop_column('posts', 'author_id')
    op.drop_index('title', 'posts')
    pass
