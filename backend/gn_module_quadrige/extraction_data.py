# backend/gn_module_quadrige/extraction_data.py
import os
import time
import requests

from flask import current_app
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

from .build_query import build_extraction_query
from . import utils_backend


def extract_ifremer_data(programmes, filter_data, output_dir, monitoring_location, ts):
    """
    Lance les extractions de résultats pour chaque programme et renvoie
    une liste de fichiers ZIP (déjà téléchargés et renommés) :
    [
      {"file_name": "...zip", "url": "/quadrige/output_data/<extraction_id>/<file>.zip"},
      ...
    ]
    """
    os.makedirs(output_dir, exist_ok=True)

    from geonature.utils.config import config as gn_config
    cfg = gn_config["QUADRIGE"]
    graphql_url = cfg["graphql_url"]
    access_token = cfg["access_token"]

    transport = RequestsHTTPTransport(
        url=graphql_url,
        verify=True,
        headers={"Authorization": f"token {access_token}"},
    )
    client = Client(transport=transport, fetch_schema_from_transport=False)

    results = []

    status_query = gql("""
        query getStatus($id: Int!) {
            getExtraction(id: $id) {
                status
                fileUrl
                error
            }
        }
    """)

    current_app.logger.info(f"[DATA] filter_data = {filter_data}")


    for prog in programmes:
        current_app.logger.info(f"[extract_ifremer_data] Programme : {prog}")
        current_app.logger.info(f"[DATA] filter_data = {filter_data}")


        # 1) Lancer la tâche
        try:
            execute_query = build_extraction_query(prog, filter_data)
            response = client.execute(execute_query)
            task_id = response["executeResultExtraction"]["id"]
        except Exception as e:
            current_app.logger.error(f"   ❌ Erreur lancement extraction {prog} : {e}")
            continue

        # 2) Polling
        file_url = None
        MAX_WAIT = 300
        start = time.time()

        while file_url is None:
            if time.time() - start > MAX_WAIT:
                raise TimeoutError(f"Extraction Ifremer trop longue (programme {prog})")

            status_response = client.execute(status_query, variable_values={"id": task_id})
            extraction = status_response["getExtraction"]
            status = extraction["status"]

            if status in ["SUCCESS", "WARNING"]:
                file_url = extraction["fileUrl"]
                warning_message = extraction.get("error")
            elif status in ["PENDING", "RUNNING"]:
                time.sleep(2)
            else:
                raise RuntimeError(extraction.get("error") or f"Statut inattendu: {status}")



        # 3) Download + rename
        # Nom demandé : data_<monitoringLocation>_<date>_<programme>.zip
        safe_ml = utils_backend.safe_slug(monitoring_location)
        safe_prog = utils_backend.safe_slug(prog)
        filename = f"data_{safe_ml}_{ts}_{safe_prog}.zip"
        local_path = os.path.join(output_dir, filename)

        current_app.logger.info(f"[DATA] Téléchargement ZIP: {file_url}")



        try:
            r = requests.get(
            file_url,
            headers={"Authorization": f"token {access_token}"},
            timeout=120,
            stream=True,
        )
            r.raise_for_status()
            
            with open(local_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

        except Exception as e:
            current_app.logger.warning(f"   ⚠️ Erreur téléchargement {prog} : {e}")
            continue

        results.append({
            "file_name": filename,
            "url": None,
            "status": status,
            "warning": warning_message if status == "WARNING" else None,
        })

    return results
