"""empty message

Revision ID: 9473733ddc93
Revises: ec6bb7cd8fb7
Create Date: 2024-06-11 16:36:41.674622

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9473733ddc93'
down_revision = 'ec6bb7cd8fb7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('encomenda',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('utilizadorId', sa.Integer(), nullable=True),
    sa.Column('aberta', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('linhaEncomenda',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('encomendaId', sa.Integer(), nullable=True),
    sa.Column('artigoId', sa.Integer(), nullable=True),
    sa.Column('quantidade', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['encomendaId'], ['encomenda.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('linhaEncomenda')
    op.drop_table('encomenda')
    # ### end Alembic commands ###