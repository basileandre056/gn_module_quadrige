# backend/gn_module_quadrige/blueprint.py
from flask import Blueprint

from .routes import init_routes

# Nom = MODULE_CODE, url_prefix = chemin sous l’API GN
#peut être qu'il faudra supprimer le préfixe /quadrige plus tard :: , url_prefix="/quadrige"
blueprint = Blueprint("quadrige", __name__)

# Enregistrement des routes définies dans routes.py
init_routes(blueprint)
