"""empty message

Revision ID: 1178d6c9b5f2
Revises: b7b5b868fb5a
Create Date: 2022-11-25 23:22:45.198138

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1178d6c9b5f2'
down_revision = 'b7b5b868fb5a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('genres')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('genres',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='genres_pkey')
    )
    # ### end Alembic commands ###
