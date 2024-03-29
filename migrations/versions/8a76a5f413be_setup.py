"""Setup

Revision ID: 8a76a5f413be
Revises: 
Create Date: 2023-02-17 14:24:21.047142

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8a76a5f413be'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('guest',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('attending', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('phone', sa.String(length=20), nullable=True),
    sa.Column('diet_req', sa.String(), nullable=True),
    sa.Column('message', sa.Text(length=150), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_guest_email'), 'guest', ['email'], unique=True)
    op.create_index(op.f('ix_guest_name'), 'guest', ['name'], unique=False)
    op.create_index(op.f('ix_guest_phone'), 'guest', ['phone'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_guest_phone'), table_name='guest')
    op.drop_index(op.f('ix_guest_name'), table_name='guest')
    op.drop_index(op.f('ix_guest_email'), table_name='guest')
    op.drop_table('guest')
    # ### end Alembic commands ###
