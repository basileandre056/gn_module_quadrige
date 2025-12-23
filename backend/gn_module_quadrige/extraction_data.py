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

    os.makedirs(output_dir, exist_ok=True)

    from geonature.utils.config import config as gn_config
    cfg = gn_config["QUADRIGE"]

    transport = RequestsHTTPTransport(
        url=cfg["graphql_url"],
        verify=True,
        headers={"Authorization": f"token {cfg['access_token']}"},
        timeout=60,
    )

    client = Client(transport=transport, fetch_schema_from_transport=False)

    status_query = gql("""
        query getStatus($id: Int!) {
            getExtraction(id: $id) {
                status
                fileUrl
                error
            }
        }
    """)

    results = []

    for prog in programmes:

        current_app.logger.warning(f"[DATA] ▶ Programme = {prog}")

        # ======================
        # 1️⃣ Lancement extraction
        # ======================
        response = client.execute(
            build_extraction_query(prog, filter_data)
        )

        job = response.get("executeResultExtraction")
        if not job:
            raise RuntimeError(f"Réponse GraphQL invalide : {response}")

        job_id = job["id"]

        # ======================
        # 2️⃣ Polling
        # ======================
        start = time.time()

        while True:
            if time.time() - start > 300:
                raise TimeoutError("Timeout extraction")

            status_resp = client.execute(
                status_query,
                variable_values={"id": job_id}
            )

            extraction = status_resp["getExtraction"]
            status = extraction["status"]
            file_url = extraction.get("fileUrl")
            error_msg = extraction.get("error")

            current_app.logger.warning(
                f"[DATA] {prog} status={status} fileUrl={file_url}"
            )

            if status in ("PENDING", "RUNNING"):
                time.sleep(2)
                continue

            if status in ("SUCCESS", "WARNING"):
                break

            # ERROR / FAILED / CANCELLED
            raise RuntimeError(f"{prog} : {error_msg}")

        # ======================
        # 3️⃣ Cas WARNING sans fichier
        # ======================
        if status == "WARNING" and not file_url:
            results.append({
                "file_name": None,
                "url": None,
                "status": "WARNING",
                "warning": error_msg,
                "programme": prog,
            })
            continue

        if status == "SUCCESS" and not file_url:
            raise RuntimeError(f"{prog} : SUCCESS sans fileUrl")


        # ======================
        # 4️⃣ Téléchargement fichier
        # ======================
        filename = f"data_{utils_backend.safe_slug(monitoring_location)}_{ts}_{utils_backend.safe_slug(prog)}.zip"
        local_path = os.path.join(output_dir, filename)

        r = requests.get(
            file_url,
            headers={"Authorization": f"token {cfg['access_token']}"},
            timeout=120
        )
        r.raise_for_status()

        with open(local_path, "wb") as f:
            f.write(r.content)

        results.append({
            "file_name": filename,
            "url": None,  # complété dans la route
            "status": status,
            "warning": None,
        })

    return results
