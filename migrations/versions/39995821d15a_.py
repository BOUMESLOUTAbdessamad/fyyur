"""empty message

Revision ID: 39995821d15a
Revises: 8be54c2a4d23
Create Date: 2022-11-25 23:51:48.704154

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '39995821d15a'
down_revision = '8be54c2a4d23'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('shows',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('artist_id', sa.Integer(), nullable=True),
    sa.Column('venue_id', sa.Integer(), nullable=True),
    sa.Column('start_time', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('shows')
    # ### end Alembic commands ###
