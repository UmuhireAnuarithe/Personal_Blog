"""Initial Migration

Revision ID: 80067999a5e9
Revises: 2238c19363a7
Create Date: 2019-09-26 17:28:45.963645

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '80067999a5e9'
down_revision = '2238c19363a7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blogs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('blog_title', sa.String(), nullable=True),
    sa.Column('blog_content', sa.String(length=500), nullable=True),
    sa.Column('posted', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['authors.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('blogs')
    # ### end Alembic commands ###
