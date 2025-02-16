"""init

Revision ID: eb10e287427a
Revises: 
Create Date: 2025-02-10 17:41:08.385497

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'eb10e287427a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('books',
    sa.Column('uid', sa.UUID(), nullable=False),
    sa.Column('title', sqlmodel.sql.sqltypes.AutoString(length=100), nullable=False),
    sa.Column('author', sqlmodel.sql.sqltypes.AutoString(length=100), nullable=False),
    sa.Column('publisher', sqlmodel.sql.sqltypes.AutoString(length=100), nullable=False),
    sa.Column('published_date', sa.Date(), nullable=False),
    sa.Column('page_count', sa.Integer(), nullable=False),
    sa.Column('language', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(), nullable=True),
    sa.PrimaryKeyConstraint('uid')
    )
    op.create_table('users',
    sa.Column('uid', sa.UUID(), nullable=False),
    sa.Column('username', sa.String(length=100), nullable=True),
    sa.Column('password_hash', sa.LargeBinary(), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('first_name', sa.String(length=120), nullable=True),
    sa.Column('last_name', sa.String(length=120), nullable=True),
    sa.Column('is_verified', sa.Boolean(), nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(), nullable=True),
    sa.PrimaryKeyConstraint('uid'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('books')
    # ### end Alembic commands ###
