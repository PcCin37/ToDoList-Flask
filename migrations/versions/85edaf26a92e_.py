"""empty message

Revision ID: 85edaf26a92e
Revises: 2ddad1e9869a
Create Date: 2022-10-30 12:58:57.578353

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '85edaf26a92e'
down_revision = '2ddad1e9869a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('question', sa.Column('assessment_title', sa.String(length=200), nullable=False))
    op.add_column('question', sa.Column('description', sa.Text(), nullable=False))
    op.drop_column('question', 'title')
    op.drop_column('question', 'content')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('question', sa.Column('content', mysql.TEXT(), nullable=False))
    op.add_column('question', sa.Column('title', mysql.VARCHAR(length=200), nullable=False))
    op.drop_column('question', 'description')
    op.drop_column('question', 'assessment_title')
    # ### end Alembic commands ###
