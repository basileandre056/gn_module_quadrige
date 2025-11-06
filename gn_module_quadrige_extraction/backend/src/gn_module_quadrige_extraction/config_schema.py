from marshmallow import Schema, fields

class QuadrigeConfigSchema(Schema):
    # Exemple de paramètres de configuration du module
    enabled = fields.Boolean(required=True, load_default=True)
    export_max_rows = fields.Integer(required=False, load_default=10000)


def get_config_schema():
    return QuadrigeConfigSchema()