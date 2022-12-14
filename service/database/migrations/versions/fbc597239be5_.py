"""empty message

Revision ID: fbc597239be5
Revises: 19ec230ac008
Create Date: 2022-11-05 13:15:48.558592

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fbc597239be5'
down_revision = '19ec230ac008'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('floor',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.add_column('analogue_flat', sa.Column('floor_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'analogue_flat', 'floor', ['floor_id'], ['id'])
    op.drop_column('analogue_flat', 'floor')
    op.add_column('flat', sa.Column('floor_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'flat', 'floor', ['floor_id'], ['id'])
    op.drop_column('flat', 'floor')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('flat', sa.Column('floor', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'flat', type_='foreignkey')
    op.drop_column('flat', 'floor_id')
    op.add_column('analogue_flat', sa.Column('floor', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'analogue_flat', type_='foreignkey')
    op.drop_column('analogue_flat', 'floor_id')
    op.drop_table('floor')
    # ### end Alembic commands ###
