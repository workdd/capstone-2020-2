"""add_name

Revision ID: 4438a99e7cca
Revises: e86b01d929e7
Create Date: 2020-06-01 18:52:10.171429

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4438a99e7cca'
down_revision = 'e86b01d929e7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('login_expiry', sa.Column('name', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('login_expiry', 'name')
    # ### end Alembic commands ###
