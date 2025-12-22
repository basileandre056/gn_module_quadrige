# backend/gn_module_quadrige/extraction_programs.py

import time

from flask import current_app
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport


def extract_programs(filter_data: dict):
    """
    Lance une extraction de programmes et retourne l’URL CSV fournie par Ifremer.
    """

   # 🔥 Lecture de la configuration TOML du module (import LAZY)
    from geonature.utils.config import config as gn_config
    cfg = gn_config["QUADRIGE"]

    graphql_url = cfg["graphql_url"]
    access_token = cfg["access_token"]

    # Client GraphQL Ifremer
    transport = RequestsHTTPTransport(
        url=graphql_url,
        verify=True,
        headers={"Authorization": f"token {access_token}"},
    )
    client = Client(transport=transport, fetch_schema_from_transport=False)

    name = filter_data.get("name", "Extraction Programmes")
    monitoring_location = filter_data.get("monitoringLocation", "")

    if not monitoring_location:
        raise ValueError("Le champ 'monitoringLocation' est vide — requête annulée.")

    query = gql(f"""
        query {{
          executeProgramExtraction(
            filter: {{
              name: "{name}"
              criterias: [{{
                monitoringLocation: {{ searchText: "{monitoring_location}" }}
              }}]
            }}
          ) {{
            id
            name
            startDate
            status
          }}
        }}
    """)

    try:
        response = client.execute(query)
        task = response["executeProgramExtraction"]

        task_id = task["id"]
        current_app.logger.info(
            f"[extract_programs] ✅ Extraction lancée (id={task_id}, nom={task['name']})"
        )

    except Exception as e:
        raise RuntimeError(f"Erreur lors du lancement de l’extraction : {e}")

    # 🔁 Suivi du statut
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
        status_resp = client.execute(status_query, variable_values={"id": task_id})
        extraction = status_resp["getExtraction"]

        status = extraction["status"]
        current_app.logger.info(f"[extract_programs] Statut : {status}")

        if status == "SUCCESS":
            file_url = extraction["fileUrl"]
            current_app.logger.info(
                f"[extract_programs] ✅ Fichier disponible : {file_url}"
            )

        elif status in ["PENDING", "RUNNING"]:
            time.sleep(2)

        else:
            raise RuntimeError(f"Tâche en erreur : {extraction.get('error')}")

    return file_url
