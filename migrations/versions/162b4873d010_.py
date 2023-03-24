"""empty message

Revision ID: 162b4873d010
Revises: c972e6174632
Create Date: 2022-10-30 14:23:36.180664

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '162b4873d010'
down_revision = 'c972e6174632'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('todolist',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('assessment_title', sa.String(length=200), nullable=False),
    sa.Column('module', sa.String(length=200), nullable=False),
    sa.Column('deadline', sa.Date(), nullable=True),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('answer',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('todolist_id', sa.Integer(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['todolist_id'], ['todolist.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('answer')
    op.drop_table('todolist')
    # ### end Alembic commands ###