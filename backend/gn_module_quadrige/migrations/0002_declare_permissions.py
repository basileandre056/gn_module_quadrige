"""
Declare available permissions for QUADRIGE module

Revision ID: 0002
Revises: 0001
Create Date: 2025-11-27
"""

from alembic import op

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
        INSERT INTO
            gn_permissions.t_permissions_available (
                id_module,
                id_object,
                id_action,
                label,
                scope_filter
            )
        SELECT
            m.id_module,
            o.id_object,
            a.id_action,
            v.label,
            v.scope_filter
        FROM (
            VALUES
                ('QUADRIGE', 'QUADRIGE_ALL', 'C', False, 'Créer dans QUADRIGE'),
                ('QUADRIGE', 'QUADRIGE_ALL', 'R', True , 'Voir QUADRIGE'),
                ('QUADRIGE', 'QUADRIGE_ALL', 'U', False, 'Modifier QUADRIGE'),
                ('QUADRIGE', 'QUADRIGE_ALL', 'D', False, 'Supprimer dans QUADRIGE')
        ) AS v (module_code, object_code, action_code, scope_filter, label)
        JOIN gn_commons.t_modules m ON m.module_code = v.module_code
        JOIN gn_permissions.t_objects o ON o.code_object = v.object_code
        JOIN gn_permissions.bib_actions a ON a.code_action = v.action_code;
    """)


def downgrade():
    op.execute("""
        DELETE FROM gn_permissions.t_permissions_available pa
        USING gn_commons.t_modules m
        WHERE pa.id_module = m.id_module
          AND m.module_code = 'QUADRIGE';
    """)
