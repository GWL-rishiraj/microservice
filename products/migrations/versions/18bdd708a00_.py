"""empty message

Revision ID: 18bdd708a00
Revises: 24d2d49f346
Create Date: 2020-09-09 20:17:01.202048

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '18bdd708a00'
down_revision = '24d2d49f346'
branch_labels = None
depends_on = None


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.add_column(sa.Column('quantity', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('remaining_quantity', sa.Integer(), nullable=True))

    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.drop_column('remaining_quantity')
        batch_op.drop_column('quantity')

    ### end Alembic commands ###
