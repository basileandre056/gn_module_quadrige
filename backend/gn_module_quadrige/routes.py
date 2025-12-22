# backend/gn_module_quadrige/routes.py
import os
import requests
from flask import request, jsonify, send_from_directory, abort
import json


from .extraction_data import extract_ifremer_data
from .extraction_programs import extract_programs
from . import utils_backend




def init_routes(bp):

    @bp.route("/program-extraction", methods=["POST"])
    def recevoir_program_extraction():
        data = request.json or {}
        program_filter = data.get("filter", {})
        monitoring_location = program_filter.get("monitoringLocation", "")

        if not monitoring_location:
            return jsonify({"status": "error", "message": "monitoringLocation manquante"}), 400

        try:
            file_url = extract_programs(program_filter)

            # save last filter (pour data-extractions)
            utils_backend.sauvegarder_filtre(program_filter)

            # 1 dossier par extraction programmes
            dirname, prog_dir = utils_backend.create_programs_dir(monitoring_location)
            utils_backend.cleanup_old_dirs(utils_backend.PROGRAMS_DIR, keep=3)

            ts = dirname.split("_")[-1]  # programmes_<ml>_<ts>

            safe_ml = utils_backend.safe_slug(monitoring_location)
            brut_filename = f"programmes_{safe_ml}_{ts}_brut.csv"
            filtered_filename = f"programmes_{safe_ml}_{ts}_filtered.csv"

            brut_path = os.path.join(prog_dir, brut_filename)
            filtered_path = os.path.join(prog_dir, filtered_filename)

            r = requests.get(file_url, timeout=120)
            r.raise_for_status()
            with open(brut_path, "wb") as f:
                f.write(r.content)

            utils_backend.nettoyer_csv(brut_path, filtered_path, monitoring_location)
            programmes_json = utils_backend.csv_to_programmes_json(filtered_path)

            base_url = "/geonature/api/quadrige/programs/"
            return jsonify({
                "status": "ok",
                "fichiers_csv": [
                    {"file_name": brut_filename, "url": f"{base_url}/{dirname}/{brut_filename}"},
                    {"file_name": filtered_filename, "url": f"{base_url}/{dirname}/{filtered_filename}"},
                ],
                "programmes": programmes_json,
            }), 200

        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500

    @bp.route("/data-extractions", methods=["POST"])
    def recevoir_data_extractions():
        data = request.json or {}
        programmes = data.get("programmes", [])
        filter_data_front = data.get("filter", {})

        if not programmes:
            return jsonify({"status": "warning", "message": "Aucun programme reçu"}), 400

        last_filter = utils_backend.charger_filtre()
        monitoring_location = last_filter.get("monitoringLocation", "")
        if not monitoring_location:
            return jsonify({"status": "error", "message": "Aucune monitoringLocation sauvegardée"}), 400

        # filtre final (force monitoringLocation)
        filter_data = dict(filter_data_front)
        filter_data["monitoringLocation"] = monitoring_location

        # 1 dossier par extraction data
        extraction_id, extraction_dir = utils_backend.create_extraction_dir()
        utils_backend.cleanup_old_dirs(utils_backend.OUTPUT_DATA_DIR, keep=3)

        ts = utils_backend.now_ts()

        try:
            files = extract_ifremer_data(
                programmes=programmes,
                filter_data=filter_data,
                output_dir=extraction_dir,
                monitoring_location=monitoring_location,
                ts=ts,
            )
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500

        if not files:
            return jsonify({"status": "warning", "message": "Aucun fichier généré"}), 404

        # compléter les URLs maintenant qu'on a extraction_id
        base_url = "/geonature/api/quadrige/output_data"
        for f in files:
            f["url"] = f"{base_url}/{extraction_id}/{f['file_name']}"

        return jsonify({
            "status": "ok",
            "programmes_recus": programmes,
            "filtre_utilise": filter_data,
            "fichiers_zip": files,
        }), 200

    # ✅ téléchargement direct (attachment)
    @bp.route("/programs/<path:subpath>", methods=["GET"])
    def download_programs_file(subpath):
        # subpath = "<dirname>/<filename>"
        full_path = os.path.join(utils_backend.PROGRAMS_DIR, subpath)
        if not os.path.isfile(full_path):
            abort(404)
        directory = os.path.dirname(full_path)
        filename = os.path.basename(full_path)
        return send_from_directory(directory, filename, as_attachment=True)

    @bp.route("/output_data/<path:subpath>", methods=["GET"])
    def download_output_data(subpath):
        # subpath = "<extraction_id>/<filename>"
        full_path = os.path.join(utils_backend.OUTPUT_DATA_DIR, subpath)
        if not os.path.isfile(full_path):
            abort(404)
        directory = os.path.dirname(full_path)
        filename = os.path.basename(full_path)
        return send_from_directory(directory, filename, as_attachment=True)

    @bp.route("/last-programmes", methods=["GET"])
    def get_last_programmes():
        base_dir = utils_backend.PROGRAMS_DIR

        if not os.path.exists(base_dir):
            return jsonify({"status": "empty"}), 200

        # dossiers triés par date (desc)
        dirs = sorted(
            [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))],
            key=lambda d: os.path.getmtime(os.path.join(base_dir, d)),
            reverse=True,
        )


        if not dirs:
            return jsonify({"status": "empty"}), 200

        last_dir = dirs[0]
        last_dir_path = os.path.join(base_dir, last_dir)

        fichiers_csv = []
        filtered_csv = None

        for f in os.listdir(last_dir_path):
            if f.endswith(".csv"):
                fichiers_csv.append({
                    "file_name": f,
                    "url": f"/quadrige/programs/{last_dir}/{f}",
                })
                if "filtered" in f:
                    filtered_csv = os.path.join(last_dir_path, f)

        programmes = (
            utils_backend.csv_to_programmes_json(filtered_csv)
            if filtered_csv and os.path.exists(filtered_csv)
            else []
        )

        # monitoringLocation déduite du nom du dossier
        # programmes_<location>_<timestamp>
        parts = last_dir.split("_")
        meta_path = os.path.join(last_dir_path, "meta.json")
        monitoring_location = None
        if os.path.exists(meta_path):
            with open(meta_path) as f:
                monitoring_location = json.load(f).get("monitoringLocation")


        return jsonify({
            "status": "ok" if programmes else "empty",
            "monitoringLocation": monitoring_location,
            "programmes": programmes,
            "fichiers_csv": fichiers_csv,
        }), 200


    @bp.route("/filtrage_seul", methods=["POST"])
    def filtrage_seul():
        data = request.json or {}
        program_filter = data.get("filter", {})

        # Si pas de filtre fourni → on reprend le dernier
        if not program_filter:
            program_filter = utils_backend.charger_filtre()

        monitoring_location = program_filter.get("monitoringLocation", "")
        if not monitoring_location:
            return jsonify({
                "status": "empty",
                "message": "Aucun filtre disponible",
                "programmes": [],
                "fichiers_csv": [],
            }), 200

        base_dir = utils_backend.PROGRAMS_DIR

        if not os.path.exists(base_dir):
            return jsonify({"status": "empty"}), 200

        # Dernier dossier programmes
        dirs = sorted(
            [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))],
            key=lambda d: os.path.getmtime(os.path.join(base_dir, d)),
            reverse=True,
        )

        if not dirs:
            return jsonify({"status": "empty"}), 200

        last_dir = dirs[0]
        last_dir_path = os.path.join(base_dir, last_dir)

        brut_csv = None
        filtered_csv = None

        for f in os.listdir(last_dir_path):
            if f.endswith("_brut.csv"):
                brut_csv = os.path.join(last_dir_path, f)
            if f.endswith("_filtered.csv"):
                filtered_csv = os.path.join(last_dir_path, f)

        if not brut_csv or not os.path.exists(brut_csv):
            return jsonify({
                "status": "warning",
                "message": "CSV brut introuvable",
                "programmes": [],
                "fichiers_csv": [],
            }), 200

        # Re-filtrage
        utils_backend.nettoyer_csv(
            brut_csv,
            filtered_csv,
            monitoring_location,
        )

        programmes = utils_backend.csv_to_programmes_json(filtered_csv)

        fichiers_csv = [
            {
                "file_name": os.path.basename(brut_csv),
                "url": f"/quadrige/programs/{last_dir}/{os.path.basename(brut_csv)}",
            },
            {
                "file_name": os.path.basename(filtered_csv),
                "url": f"/quadrige/programs/{last_dir}/{os.path.basename(filtered_csv)}",
            },
        ]

        return jsonify({
            "status": "ok",
            "message": "Filtrage relancé avec succès",
            "monitoringLocation": monitoring_location,
            "programmes": programmes,
            "fichiers_csv": fichiers_csv,
        }), 200



    @bp.route("/config", methods=["GET"])
    def get_config():
        """
        Renvoie la configuration Quadrige :
          - si aucune config TOML -> renvoie {} + warning
          - si config TOML présente -> vérification de validité
        """
        from geonature.utils.config import config as gn_config
    
        cfg = gn_config.get("QUADRIGE")
    
        if not cfg:
            return jsonify({
                "status": "warning",
                "message": (
                    "Aucune configuration Quadrige chargée. "
                    "Le fichier quadrige_config.toml est absent ou vide."
                ),
                "config": {}
            }), 200
    
        # ------------------------------------
        # 🔍 Vérification facultative du TOML
        # ------------------------------------
        errors = []
    
        # 1) graphql_url obligatoire si TOML existe
        if not cfg.get("graphql_url"):
            errors.append("graphql_url manquant")
    
        # 2) access_token obligatoire si TOML existe
        if not cfg.get("access_token"):
            errors.append("access_token manquant")
    
        # 3) locations doit être une liste de dicts
        locations = cfg.get("locations")
        if locations is not None and not isinstance(locations, list):
            errors.append("locations doit être une liste")
        elif isinstance(locations, list):
            for loc in locations:
                if not isinstance(loc, dict) or "code" not in loc or "label" not in loc:
                    errors.append("locations : un élément doit contenir {code, label}")
                    break
                
        # 4) extractable_fields doit être une liste de chaînes
        fields = cfg.get("extractable_fields")
        if fields is not None and not isinstance(fields, list):
            errors.append("extractable_fields doit être une liste")
        elif isinstance(fields, list):
            if not all(isinstance(f, str) for f in fields):
                errors.append("extractable_fields doit contenir uniquement des chaînes")
    
        # ------------------------------------
        #  Résultat final
        # ------------------------------------
        if errors:
            return jsonify({
                "status": "warning",
                "message": "La configuration Quadrige comporte des incohérences.",
                "errors": errors,
                "config": cfg
            }), 200
    
        # Config OK
        return jsonify({
            "status": "ok",
            "config": cfg
        }), 200
