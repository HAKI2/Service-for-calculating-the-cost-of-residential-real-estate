"""empty message

Revision ID: 62937efd4e8c
Revises: 
Create Date: 2022-10-29 13:17:37.445544

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '62937efd4e8c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=80), nullable=False),
    sa.Column('last_name', sa.String(length=80), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('id_admin', sa.Boolean(), nullable=False),
    sa.Column('date_joined', sa.DateTime(), nullable=False),
    sa.Column('last_login', sa.DateTime(), nullable=False),
    sa.Column('password', sa.String(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###
