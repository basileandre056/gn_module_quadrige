"""
Create QUADRIGE default permission object

Revision ID: 0001
Revises:
Create Date: 2025-11-27
"""

from alembic import op

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Ajout de l'objet principal QUADRIGE
    op.execute("""
        INSERT INTO gn_permissions.t_objects (code_object, label, description)
        VALUES ('QUADRIGE_ALL', 'Tous', 'Objet principal pour le module QUADRIGE')
    """)
    

def downgrade():
    op.execute("""
        DELETE FROM gn_permissions.t_objects
        WHERE code_object = 'QUADRIGE_ALL'
    """)
