"""Add foreign keys, relationships and rules

Revision ID: 2229d2ac7cb9
Revises: 33d020f8ef2c
Create Date: 2025-04-07 10:00:26.069815

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2229d2ac7cb9'
down_revision = '33d020f8ef2c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('appearances', schema=None) as batch_op:
        batch_op.add_column(sa.Column('guest_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('episode_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(batch_op.f('fk_appearances_guest_id_guests'), 'guests', ['guest_id'], ['id'])
        batch_op.create_foreign_key(batch_op.f('fk_appearances_episode_id_episodes'), 'episodes', ['episode_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('appearances', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_appearances_episode_id_episodes'), type_='foreignkey')
        batch_op.drop_constraint(batch_op.f('fk_appearances_guest_id_guests'), type_='foreignkey')
        batch_op.drop_column('episode_id')
        batch_op.drop_column('guest_id')

    # ### end Alembic commands ###
