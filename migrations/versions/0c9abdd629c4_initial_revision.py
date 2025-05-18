"""initial revision

Revision ID: 0c9abdd629c4
Revises: 
Create Date: 2025-05-18 14:34:16.872780

"""
from typing import Sequence, Union, Text

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '0c9abdd629c4'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('title', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('content', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('published', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column(
            'created_at', 
            sa.TIMESTAMP(timezone=True), 
            nullable=False,
            server_default=sa.text("now()")),
    )

# op.create_table(
#         'post',
#         sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
#         sa.Column('title', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
#         sa.Column('content', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
#         sa.Column('published', sa.Boolean(), server_default=sa.text("true"), nullable=False),
#         sa.Column('rating', sa.Float(), server_default=sa.text("0.0"), nullable=True),
#         sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
#         sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
#         sa.Column('author_id', sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
#     )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('posts')
    pass
