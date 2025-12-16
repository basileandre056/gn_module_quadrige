"""
Declare QUADRIGE permissions

Revision ID: 0002_quadrige_permissions
Revises: 0001_quadrige_init
Create Date: 2025-12-16
"""

from alembic import op

revision = "0002_quadrige_permissions"
down_revision = "0001_quadrige_init"
branch_labels = None
depends_on = None


def upgrade():

    op.execute("""
        INSERT INTO gn_permissions.t_permissions_available (
            id_module,
            id_object,
            id_action,
            scope_filter,
            label
        )
        SELECT
            m.id_module,
            o.id_object,
            a.id_action,
            v.scope_filter,
            v.label
        FROM (
            VALUES
                ('QUADRIGE', 'ALL', 'R', false, 'Accéder au module Quadrige'),
                ('QUADRIGE', 'ALL', 'C', false, 'Lancer une extraction Quadrige'),
                ('QUADRIGE', 'ALL', 'U', false, 'Modifier les paramètres Quadrige'),
                ('QUADRIGE', 'ALL', 'D', false, 'Supprimer une extraction Quadrige')
        ) AS v (module_code, object_code, action_code, scope_filter, label)
        JOIN gn_commons.t_modules m ON m.module_code = v.module_code
        JOIN gn_permissions.t_objects o ON o.code_object = v.object_code
        JOIN gn_permissions.bib_actions a ON a.code_action = v.action_code
        WHERE NOT EXISTS (
            SELECT 1
            FROM gn_permissions.t_permissions_available pa
            WHERE pa.id_module = m.id_module
              AND pa.id_object = o.id_object
              AND pa.id_action = a.id_action
        );
    """)


def downgrade():
    op.execute("""
        DELETE FROM gn_permissions.t_permissions_available
        WHERE id_module = (
            SELECT id_module FROM gn_commons.t_modules WHERE module_code = 'QUADRIGE'
        );
    """)
