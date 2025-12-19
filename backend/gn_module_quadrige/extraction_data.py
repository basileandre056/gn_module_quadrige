# backend/gn_module_quadrige/extraction_data.py

import os
import time
import requests

from flask import current_app
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

from .utils_backend import OUTPUT_DATA_DIR
from .build_query import build_extraction_query


def extract_ifremer_data(programmes, filter_data):
    """
    Lance les extractions de résultats pour chaque programme et renvoie
    la liste des URLs de fichiers ZIP fournis par Ifremer.
    """

    # 🔥 Lecture de la configuration TOML du module
    # 🔥 Lecture de la configuration TOML du module (import LAZY pour éviter la boucle)
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

    download_links = []
    os.makedirs(OUTPUT_DATA_DIR, exist_ok=True)

    for p in programmes:
        current_app.logger.info(f"[extract_ifremer_data] Programme : {p}")

        # 1) Lancer la tâche d’extraction
        try:
            execute_query = build_extraction_query(p, filter_data)
            response = client.execute(execute_query)

            task_id = response["executeResultExtraction"]["id"]
            current_app.logger.info(f"   Extraction lancée (id: {task_id})")

        except Exception as e:
            current_app.logger.error(f"   ❌ Erreur lors de l'extraction {p} : {e}")
            continue

        # 2) Suivi du statut
        status_query = gql("""
            query getStatus($id: Int!) {
                getExtraction(id: $id) {
                    status
                    fileUrl
                    error
                }
            }
        """)

        file_url = None
        while file_url is None:
            status_response = client.execute(
                status_query, variable_values={"id": task_id}
            )
            extraction = status_response["getExtraction"]
            status = extraction["status"]

            current_app.logger.info(f"    Statut: {status}")

            if status == "SUCCESS":
                file_url = extraction["fileUrl"]
                current_app.logger.info(f"     ✅ Fichier disponible : {file_url}")

            elif status in ["PENDING", "RUNNING"]:
                time.sleep(2)

            else:
                current_app.logger.error(
                    f"     ❌ Tâche en erreur : {extraction.get('error')}"
                )
                break

        if not file_url:
            continue

        # 3) (Optionnel) Téléchargement local
        zip_path = os.path.join(OUTPUT_DATA_DIR, os.path.basename(file_url))

        try:
            r = requests.get(file_url)
            r.raise_for_status()

            with open(zip_path, "wb") as f:
                f.write(r.content)

            current_app.logger.info(
                f"     💾 ZIP téléchargé localement : {zip_path}"
            )

        except Exception as e:
            current_app.logger.warning(
                f"     ⚠️ Erreur lors du téléchargement : {e}"
            )

        download_links.append(file_url)

    return download_links
