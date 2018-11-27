"""empty message

Revision ID: 6a3910dd4049
Revises: 8d1933edb09b
Create Date: 2018-11-27 09:50:52.094075

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6a3910dd4049'
down_revision = '8d1933edb09b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('athlete', sa.Column('high_school', sa.String(length=120), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('athlete', 'high_school')
    # ### end Alembic commands ###
