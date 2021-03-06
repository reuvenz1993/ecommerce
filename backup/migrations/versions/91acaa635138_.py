"""empty message

Revision ID: 91acaa635138
Revises: 25946997c0e6
Create Date: 2020-01-09 06:40:24.538099

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '91acaa635138'
down_revision = '25946997c0e6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('buyer_id', sa.Integer(), nullable=False),
    sa.Column('supplier_id', sa.Integer(), nullable=False),
    sa.Column('order_time', sa.DateTime(), nullable=True),
    sa.Column('qty', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(length=256), nullable=True),
    sa.Column('unit_price', sa.Numeric(), nullable=False),
    sa.Column('total_price', sa.Numeric(), nullable=False),
    sa.ForeignKeyConstraint(['buyer_id'], ['buyers.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.ForeignKeyConstraint(['supplier_id'], ['suppliers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('reviews',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('stars', sa.Integer(), nullable=True),
    sa.Column('review_content', sa.String(length=512), nullable=True),
    sa.Column('review_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('the_orders')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('the_orders',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('product_id', sa.INTEGER(), nullable=False),
    sa.Column('buyer_id', sa.INTEGER(), nullable=False),
    sa.Column('supplier_id', sa.INTEGER(), nullable=False),
    sa.Column('order_time', sa.DATETIME(), nullable=True),
    sa.Column('qty', sa.INTEGER(), nullable=False),
    sa.Column('status', sa.VARCHAR(length=256), nullable=True),
    sa.Column('unit_price', sa.NUMERIC(), nullable=False),
    sa.Column('total_price', sa.NUMERIC(), nullable=False),
    sa.ForeignKeyConstraint(['buyer_id'], ['buyers.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.ForeignKeyConstraint(['supplier_id'], ['suppliers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('reviews')
    op.drop_table('orders')
    # ### end Alembic commands ###
