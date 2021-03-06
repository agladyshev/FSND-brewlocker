"""create cloudinary id field for image model

Revision ID: b3df73ced68e
Revises: 45ec5e81b21b
Create Date: 2017-09-03 23:19:39.162470

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b3df73ced68e'
down_revision = '45ec5e81b21b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('images', sa.Column('cloudinary_id', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('images', 'cloudinary_id')
    # ### end Alembic commands ###
