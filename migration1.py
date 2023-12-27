from alembic import op
import sqlalchemy as sa

revision = 'XXXX'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    
    op.add_column('groups', sa.Column('additional_info', sa.String(length=255), nullable=True))
    op.add_column('subjects', sa.Column('additional_info', sa.String(length=255), nullable=True))

def downgrade():
    op.drop_column('groups', 'additional_info')
    op.drop_column('subjects', 'additional_info')
