"""priority

Revision ID: db15a12216b3
Revises: d28967d221d1
Create Date: 2022-03-24 12:58:06.167566

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'db15a12216b3'
down_revision = 'd28967d221d1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('reports', sa.Column('priority', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('reports', 'priority')
    # ### end Alembic commands ###