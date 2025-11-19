# backend/gn_module_quadrige/config_schema_toml.py
"""
Schéma Marshmallow pour la configuration TOML du module Quadrige.

La classe doit impérativement s'appeler GnModuleSchemaConf.
Les valeurs réelles seront surchargées par config/config_gn_module.toml
dans l’installation GeoNature.
"""

# Important pour la PROD :

#Le fichier utilisé sur le serveur ne sera pas ton module_code_config.toml, mais le fichier central de GN (souvent config/config_gn_module.toml ou équivalent, géré par l’admin GN).
#
#Dedans, il faudra une section :
#
#[quadrige]
#graphql_url = "https://quadrige-core.ifremer.fr/graphql/public"
#access_token = "TON_TOKEN_DE_PROD"


from marshmallow import Schema, fields

class GnModuleSchemaConf(Schema):
    graphql_url = fields.Url(
        missing="https://quadrige-core.ifremer.fr/graphql/public"
    )
    access_token = fields.String(
        required=True,
        description="Token d'accès Ifremer pour les extractions GraphQL"
    )

