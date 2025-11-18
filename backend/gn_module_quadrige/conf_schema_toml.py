# backend/gn_module_quadrige/conf_schema_toml.py
"""
Schéma Marshmallow pour la configuration TOML du module Quadrige.

La classe doit impérativement s'appeler GnModuleSchemaConf.
Les valeurs réelles seront surchargées par config/config_gn_module.toml
dans l’installation GeoNature.
"""

from marshmallow import Schema, fields

class GnModuleSchemaConf(Schema):
    graphql_url = fields.Url(
        missing="https://quadrige-core.ifremer.fr/graphql/public"
    )
    access_token = fields.String(
        required=True,
        description="Token d'accès Ifremer pour les extractions GraphQL"
    )

