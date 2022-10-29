"""empty message

Revision ID: 7aaa1d5bf439
Revises: 4d3e6d5b4bfe
Create Date: 2022-10-29 18:28:36.222891

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7aaa1d5bf439'
down_revision = '4d3e6d5b4bfe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('request_pool', sa.Column('date_created', sa.DateTime(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('request_pool', 'date_created')
    # ### end Alembic commands ###