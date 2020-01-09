"""empty message

Revision ID: 25946997c0e6
Revises: 
Create Date: 2020-01-09 06:25:58.779039

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '25946997c0e6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('buyers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=False),
    sa.Column('name', sa.String(length=256), nullable=True),
    sa.Column('address', sa.String(length=256), nullable=True),
    sa.Column('photo', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('suppliers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=False),
    sa.Column('name', sa.String(length=256), nullable=True),
    sa.Column('type_of', sa.String(length=256), nullable=True),
    sa.Column('address', sa.String(length=256), nullable=True),
    sa.Column('photo', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=False),
    sa.Column('photo', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('content', sa.String(length=2048), nullable=False),
    sa.Column('time', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=256), nullable=False),
    sa.Column('desc', sa.String(length=1024), nullable=True),
    sa.Column('supplier_id', sa.Integer(), nullable=False),
    sa.Column('product_type', sa.String(length=256), nullable=True),
    sa.Column('product_sub_type', sa.String(length=256), nullable=True),
    sa.Column('brand', sa.String(length=256), nullable=True),
    sa.Column('price', sa.Numeric(), nullable=False),
    sa.Column('picture', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['supplier_id'], ['suppliers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('the_orders',
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
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('the_orders')
    op.drop_table('products')
    op.drop_table('posts')
    op.drop_table('users')
    op.drop_table('suppliers')
    op.drop_table('buyers')
    # ### end Alembic commands ###
