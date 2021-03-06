"""change foregin key

Revision ID: cc4ffab75f5f
Revises: 117e205f9e15
Create Date: 2018-10-23 21:17:11.702899

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cc4ffab75f5f'
down_revision = '117e205f9e15'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('tickets_user_id_fkey', 'tickets', type_='foreignkey')
    op.create_foreign_key(None, 'tickets', 'users', ['user_id'], ['username'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'tickets', type_='foreignkey')
    op.create_foreign_key('tickets_user_id_fkey', 'tickets', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###
