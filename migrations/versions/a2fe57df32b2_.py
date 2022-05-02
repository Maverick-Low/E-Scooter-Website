"""empty message

Revision ID: a2fe57df32b2
Revises: a734881592c3
Create Date: 2022-05-01 22:55:13.191916

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a2fe57df32b2'
down_revision = 'a734881592c3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bookings', sa.Column('email', sa.String(length=60), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('bookings', 'email')
    # ### end Alembic commands ###