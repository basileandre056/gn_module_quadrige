from marshmallow import Schema, fields

class PermissionLevelSchema(Schema):
    module = fields.String(required=True)


class GnModuleSchemaConf(Schema):

    # --- FRONTEND ---
    MODULE_CODE = fields.String(missing="QUADRIGE")
    MODULE_URL = fields.String(missing="/quadrige")
    TITLE_MODULE = fields.String(missing="Module Quadrige")
    DESCRIPTION_MODULE = fields.String(missing="Extraction Quadrige – Ifremer")
    ICON = fields.String(missing="assets/quadrige/picto.png")

    PERMISSION_LEVEL = fields.Nested(
        PermissionLevelSchema,
        missing=lambda: {"module": "QUADRIGE_MODULES"}
    )

    # --- BACKEND ---
    graphql_url = fields.Url(required=True)
    access_token = fields.String(required=True)

    locations = fields.List(
        fields.Dict(keys=fields.String(), values=fields.String()),
        missing=list
    )

    extractable_fields = fields.List(
        fields.String(),
        missing=list
    )
