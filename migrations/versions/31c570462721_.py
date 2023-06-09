"""empty message

Revision ID: 31c570462721
Revises: 2315fd223d37
Create Date: 2022-11-09 21:36:53.839255

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '31c570462721'
down_revision = '2315fd223d37'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('todolist',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('assessment_title', sa.String(length=200), nullable=False),
    sa.Column('module', sa.String(length=200), nullable=False),
    sa.Column('deadline', sa.DateTime(), nullable=True),
    sa.Column('importance', sa.String(length=200), nullable=False),
    sa.Column('status', sa.String(length=200), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('todolist')
    # ### end Alembic commands ###
