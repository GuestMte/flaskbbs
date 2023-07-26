"""empty message

Revision ID: fca5da2d26ab
Revises: 5279a53e0a46
Create Date: 2023-07-24 21:07:32.504249

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fca5da2d26ab'
down_revision = '5279a53e0a46'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.String(length=100), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('_password', sa.String(length=200), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('avatar', sa.String(length=100), nullable=True),
    sa.Column('signature', sa.String(length=100), nullable=True),
    sa.Column('join_time', sa.DateTime(), nullable=True),
    sa.Column('is_staff', sa.Boolean(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###
