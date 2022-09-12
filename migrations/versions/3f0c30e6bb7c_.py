"""empty message

Revision ID: 3f0c30e6bb7c
Revises: c394c5d47879
Create Date: 2022-09-12 17:50:38.619333

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3f0c30e6bb7c'
down_revision = 'c394c5d47879'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comments', schema=None) as batch_op:
        batch_op.add_column(sa.Column('author_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(batch_op.f('fk_comments_author_id_users'), 'users', ['author_id'], ['id'], ondelete='CASCADE')

    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.create_unique_constraint(batch_op.f('uq_posts_title'), ['title'])

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.create_unique_constraint(batch_op.f('uq_users_email'), ['email'])
        batch_op.create_unique_constraint(batch_op.f('uq_users_username'), ['username'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_users_username'), type_='unique')
        batch_op.drop_constraint(batch_op.f('uq_users_email'), type_='unique')

    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_posts_title'), type_='unique')

    with op.batch_alter_table('comments', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_comments_author_id_users'), type_='foreignkey')
        batch_op.drop_column('author_id')

    # ### end Alembic commands ###
