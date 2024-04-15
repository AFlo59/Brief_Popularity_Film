"""imdb

Revision ID: 1df0a95246c9
Revises: fbdb013caba3
Create Date: 2024-04-11 07:30:31.866326

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '1df0a95246c9'
down_revision: Union[str, None] = 'fbdb013caba3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('films_imdb', sa.Column('date', sa.DATE(), nullable=True))
    op.alter_column('films_imdb', 'distributor',
               existing_type=mysql.VARCHAR(length=100),
               type_=mysql.JSON(),
               existing_nullable=True)
    op.drop_column('films_imdb', 'year')
    op.drop_column('films_imdb', 'visa')
    op.alter_column('films_jp', 'title',
               existing_type=mysql.VARCHAR(charset='utf8mb4', collation='utf8mb4_0900_ai_ci', length=255),
               nullable=False)
    op.alter_column('films_jp', 'director',
               existing_type=mysql.VARCHAR(charset='utf8mb4', collation='utf8mb4_0900_ai_ci', length=255),
               nullable=False)
    op.alter_column('films_jp', 'raw_title',
               existing_type=mysql.VARCHAR(charset='utf8mb4', collation='utf8mb4_0900_ai_ci', length=255),
               nullable=False)
    op.alter_column('films_jp', 'raw_director',
               existing_type=mysql.VARCHAR(charset='utf8mb4', collation='utf8mb4_0900_ai_ci', length=255),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('films_jp', 'raw_director',
               existing_type=mysql.VARCHAR(charset='utf8mb4', collation='utf8mb4_0900_ai_ci', length=255),
               nullable=True)
    op.alter_column('films_jp', 'raw_title',
               existing_type=mysql.VARCHAR(charset='utf8mb4', collation='utf8mb4_0900_ai_ci', length=255),
               nullable=True)
    op.alter_column('films_jp', 'director',
               existing_type=mysql.VARCHAR(charset='utf8mb4', collation='utf8mb4_0900_ai_ci', length=255),
               nullable=True)
    op.alter_column('films_jp', 'title',
               existing_type=mysql.VARCHAR(charset='utf8mb4', collation='utf8mb4_0900_ai_ci', length=255),
               nullable=True)
    op.add_column('films_imdb', sa.Column('visa', mysql.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('films_imdb', sa.Column('year', mysql.INTEGER(), autoincrement=False, nullable=True))
    op.alter_column('films_imdb', 'distributor',
               existing_type=mysql.JSON(),
               type_=mysql.VARCHAR(length=100),
               existing_nullable=True)
    op.drop_column('films_imdb', 'date')
    # ### end Alembic commands ###
