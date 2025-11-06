from flask import Blueprint, jsonify, request

# Le blueprint du module, préfixé par /quadrige-extract par ex.

def get_blueprint(config=None):
    bp = Blueprint("quadrige_extract", __name__, url_prefix="/quadrige-extract")

    @bp.get("/health")
    def health():
        return jsonify({"status": "ok", "module": "gn_module_quadrige_extraction"})

    @bp.get("/export")
    def export():
        # TODO: implémenter la logique d'extraction
        params = request.args.to_dict()
        return jsonify({"message": "export placeholder", "params": params})

    return bp