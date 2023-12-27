from alembic import op

revision = 'YYYY'
down_revision = 'XXXX'  # Зависимость от предыдущей миграции
branch_labels = None
depends_on = None

def upgrade():
    op.create_index('idx_groups_additional_info', 'groups', ['additional_info'])
    op.create_index('idx_subjects_additional_info', 'subjects', ['additional_info'])

def downgrade():
    op.drop_index('idx_groups_additional_info', 'groups')
    op.drop_index('idx_subjects_additional_info', 'subjects')
