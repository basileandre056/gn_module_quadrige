# backend/gn_module_quadrige/__init__.py
"""
Package backend du module externe GeoNature : gn_module_quadrige
"""

# Code utilisé par GeoNature pour enregistrer le module
MODULE_CODE = "quadrige"
MODULE_PICTO = "static/picto.png"
# Exposition des éléments pour les entry_points du setup.py
from .blueprint import blueprint          # Blueprint Flask (routes API)
from .config_schema_toml import GnModuleSchemaConf  # Schéma de config TOML
from . import migrations                  # Dossier Alembic (optionnel, mais prêt)
