"""empty message

Revision ID: 2315fd223d37
Revises: 70374338fae8
Create Date: 2022-11-03 22:20:42.664080

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '2315fd223d37'
down_revision = '70374338fae8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('answer')
    op.add_column('todolist', sa.Column('importance', sa.String(length=200), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('todolist', 'importance')
    op.create_table('answer',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('content', mysql.TEXT(), nullable=False),
    sa.Column('create_time', mysql.DATETIME(), nullable=True),
    sa.Column('todolist_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('author_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], name='answer_ibfk_1'),
    sa.ForeignKeyConstraint(['todolist_id'], ['todolist.id'], name='answer_ibfk_2'),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8mb3',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###