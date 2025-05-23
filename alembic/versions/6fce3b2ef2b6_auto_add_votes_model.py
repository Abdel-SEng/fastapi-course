"""auto add votes model

Revision ID: 6fce3b2ef2b6
Revises: c47ecbf163d4
Create Date: 2025-04-29 11:03:15.727827

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6fce3b2ef2b6'
down_revision = 'c47ecbf163d4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'phone_number')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('phone_number', sa.VARCHAR(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
