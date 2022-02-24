"""more_tables_added_krzysztof

Revision ID: a9c1f5f7123e
Revises: 
Create Date: 2022-02-22 14:56:46.876215

"""
from types import NoneType
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a9c1f5f7123e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('locations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('scooters',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('in_use', sa.Boolean(), nullable=True),
    sa.Column('LocationID', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['LocationID'], ['locations.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('bookings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ScooterID', sa.Integer(), nullable=True),
    sa.Column('UserID', sa.Integer(), nullable=True),
    sa.Column('numHours', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['ScooterID'], ['scooters.id'], ),
    sa.ForeignKeyConstraint(['UserID'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('bookings')
    op.drop_table('scooters')
    op.drop_table('locations')
    # ### end Alembic commands ###
