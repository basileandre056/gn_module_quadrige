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

    # ======================
    # 1️⃣ PHASE 1 — lancer toutes les extractions
    # ======================
    jobs = {}  # programme -> job_id

    for prog in programmes:
        current_app.logger.warning(f"[DATA] ▶ Lancement extraction : {prog}")

        response = client.execute(
            build_extraction_query(prog, filter_data)
        )

        job = response.get("executeResultExtraction")
        if not job:
            raise RuntimeError(f"Réponse GraphQL invalide : {response}")

        jobs[prog] = job["id"]

    # ======================
    # 2️⃣ PHASE 2 — polling global
    # ======================
    completed = {}
    start = time.time()
    MAX_WAIT = 600

    remaining = set(jobs.keys())

    while remaining:
        if time.time() - start > MAX_WAIT:
            raise TimeoutError(
                f"Timeout global extraction ({len(remaining)} programmes restants)"
            )

        for prog in list(remaining):
            job_id = jobs[prog]

            status_resp = client.execute(
                status_query,
                variable_values={"id": job_id}
            )

            extraction = status_resp["getExtraction"]
            status = extraction["status"]
            file_url = extraction.get("fileUrl")
            error_msg = extraction.get("error")

            current_app.logger.warning(
                f"[DATA] {prog} status={status}"
            )

            if status in ("PENDING", "RUNNING"):
                continue

            if status in ("SUCCESS", "WARNING"):
                completed[prog] = {
                    "status": status,
                    "file_url": file_url,
                    "error": error_msg,
                }
                remaining.remove(prog)
                continue

            # ERROR / FAILED / CANCELLED
            raise RuntimeError(f"{prog} : {error_msg}")

        time.sleep(3)  # polling global plus doux

    # ======================
    # 3️⃣ PHASE 3 — téléchargement des fichiers
    # ======================
    results = []

    for prog, data in completed.items():
        status = data["status"]
        file_url = data["file_url"]
        error_msg = data["error"]

        if status == "WARNING" and not file_url:
            results.append({
                "file_name": None,
                "url": None,
                "status": "WARNING",
                "warning": error_msg,
                "programme": prog,
            })
            continue

        if not file_url:
            raise RuntimeError(f"{prog} : pas de fileUrl")

        filename = (
            f"data_{utils_backend.safe_slug(monitoring_location)}_"
            f"{ts}_{utils_backend.safe_slug(prog)}.zip"
        )
        local_path = os.path.join(output_dir, filename)

        current_app.logger.warning(f"[DATA] ⬇ Téléchargement {prog}")

        with requests.get(
            file_url,
            headers={"Authorization": f"token {cfg['access_token']}"},
            stream=True,
            timeout=300
        ) as r:
            r.raise_for_status()
            with open(local_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

        results.append({
            "file_name": filename,
            "url": None,
            "status": status,
            "warning": None,
        })

    return results
