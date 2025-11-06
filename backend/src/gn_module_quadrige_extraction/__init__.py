from importlib import resources

MODULE_CODE = "QUADRIGE_EXTRACT"
MODULE_PICTO = None  # chemin vers un pictogramme facultatif dans assets si besoin
ALEMBIC_BRANCH = MODULE_CODE.lower()

def migrations_path():
    # Retourne un chemin utilisable par GeoNature pour les migrations du module
    return str(resources.files(__package__) / "migrations")