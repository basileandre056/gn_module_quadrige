from marshmallow import Schema, fields

class GnModuleSchemaConf(Schema):
    # --- Partie FRONTEND (ce qui ira dans ModuleConfig) ---
    MODULE_CODE = fields.String(required=False, missing="QUADRIGE")
    MODULE_URL = fields.String(required=False, missing="/quadrige")
    TITLE_MODULE = fields.String(required=False, missing="Module Quadrige")
    DESCRIPTION_MODULE = fields.String(
        required=False,
        missing="Extraction Quadrige – Ifremer"
    )
    ICON = fields.String(
        required=False,
        missing="assets/quadrige/picto.png"
    )

    # Permission frontend 
    PERMISSION_LEVEL = fields.Dict(
        required=False,
        missing=lambda: {"module": "QUADRIGE_MODULES"}
    )

    # --- Partie BACKEND Quadrige ---
    graphql_url = fields.Url(required=False, allow_none=True)
    access_token = fields.String(required=False, allow_none=True)

    locations = fields.List(
        fields.Dict(),
        required=False,
        missing=list,   # [] par défaut
    )

    extractable_fields = fields.List(
        fields.String(),
        required=False,
        missing=list,   # [] par défaut
    )
