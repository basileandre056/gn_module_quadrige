# backend/gn_module_quadrige/extraction_programs.py
import time
from flask import current_app
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport


def extract_programs(filter_data: dict):
    from geonature.utils.config import config as gn_config
    cfg = gn_config["QUADRIGE"]

    graphql_url = cfg["graphql_url"]
    access_token = cfg["access_token"]

    transport = RequestsHTTPTransport(
        url=graphql_url,
        verify=True,
        headers={"Authorization": f"token {access_token}"},
        timeout=60,
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

    response = client.execute(query)
    task = response["executeProgramExtraction"]
    task_id = task["id"]

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
    MAX_WAIT = 300
    start = time.time()

    sleep = 2

    while file_url is None:
        if time.time() - start > MAX_WAIT:
            raise TimeoutError("Extraction programmes trop longue")

        status_resp = client.execute(status_query, variable_values={"id": task_id})
        extraction = status_resp["getExtraction"]
        status = extraction["status"]

        if status in ["SUCCESS", "WARNING"]:
            file_url = extraction["fileUrl"]
            current_app.logger.warning(
                f"[PROGRAM EXTRACTION] status={status} error={extraction.get('error')}"
            )
        elif status in ["PENDING", "RUNNING"]:
            time.sleep(sleep)
            sleep = min(sleep + 1, 10)
        else:
            raise RuntimeError(f"Tâche en erreur : {extraction.get('error')}")

    return file_url
