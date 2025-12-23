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

    current_app.logger.warning(f"[DEBUG] programmes = {programmes}")
    
    for prog in programmes:
        current_app.logger.warning(f"[DEBUG] === PROGRAMME {prog} ===")
    
        try:
            execute_query = build_extraction_query(prog, filter_data)
            response = client.execute(execute_query)
            task_id = response["executeResultExtraction"]["id"]
            current_app.logger.warning(f"[DEBUG] task_id={task_id}")
        except Exception:
            current_app.logger.exception("[DEBUG] Erreur lancement extraction")
            continue
    
        file_url = None
        status = None
        start = time.time()
    
        while file_url is None:
            if time.time() - start > 300:
                raise TimeoutError("Timeout extraction")
    
            status_response = client.execute(status_query, variable_values={"id": task_id})
            extraction = status_response["getExtraction"]
    
            status = extraction["status"]
            file_url = extraction["fileUrl"]
    
            current_app.logger.warning(
                f"[DEBUG] polling prog={prog} status={status} fileUrl={file_url}"
            )
    
            if status in ["PENDING", "RUNNING"]:
                time.sleep(2)
            else:
                break
    
        if not file_url:
            current_app.logger.warning(f"[DEBUG] PAS DE fileUrl pour {prog}")
            continue
    
        try:
            current_app.logger.warning(f"[DEBUG] Téléchargement {file_url}")
            r = requests.get(file_url, headers={"Authorization": f"token {access_token}"}, timeout=120)
            r.raise_for_status()
    
            with open(local_path, "wb") as f:
                f.write(r.content)
    
        except Exception:
            current_app.logger.exception("[DEBUG] Erreur téléchargement")
            continue

        results.append({
            "file_name": filename,
            "url": None,
            "status": status,
            "warning": warning_message if status == "WARNING" else None,
        })

    return results
