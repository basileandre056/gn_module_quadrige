import os
import time

import pandas as pd
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from flask import current_app


def extract_programs(filter_data: dict):
    """
    Lance une extraction de programmes et retourne l’URL CSV fournie par Ifremer.
    """

    # 🔥 Récupération de la configuration du module (TOML)
    conf = current_app.config["GN_MODULES"]["quadrige"]
    graphql_url = conf["graphql_url"]
    access_token = conf["access_token"]

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

    query = gql(
        f"""
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
    """
    )

    try:
        response = client.execute(query)
        task = response["executeProgramExtraction"]
        task_id = task["id"]
        print(
            f"[extract_programs] ✅ Extraction lancée (id={task_id}, nom={task['name']})"
        )
    except Exception as e:
        raise RuntimeError(f"Erreur lors du lancement de l’extraction : {e}")

    # Suivi du statut
    status_query = gql(
        """
    query getStatus($id: Int!) {
        getExtraction(id: $id) {
            status
            fileUrl
            error
        }
    }
    """
    )

    file_url = None
    while file_url is None:
        status_resp = client.execute(status_query, variable_values={"id": task_id})
        extraction = status_resp["getExtraction"]
        status = extraction["status"]
        print(f"[extract_programs] Statut : {status}")

        if status == "SUCCESS":
            file_url = extraction["fileUrl"]
            print(f"[extract_programs] ✅ Fichier disponible : {file_url}")
        elif status in ["PENDING", "RUNNING"]:
            time.sleep(2)
        else:
            raise RuntimeError(f"Tâche en erreur : {extraction.get('error')}")

    return file_url


# (le reste du fichier ne change pas)
