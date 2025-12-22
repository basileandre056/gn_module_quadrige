# backend/gn_module_quadrige/utils_backend.py
import os
import json
import datetime
import tempfile
import uuid
import shutil
import re
from typing import Tuple

BASE_DIR = os.path.join(tempfile.gettempdir(), "quadrige_module")
MEMORY_DIR = os.path.join(BASE_DIR, "memory")
OUTPUT_DATA_DIR = os.path.join(BASE_DIR, "output_data")
PROGRAMS_DIR = os.path.join(BASE_DIR, "programs")
LAST_FILTER_FILE = os.path.join(MEMORY_DIR, "last_filter.json")

os.makedirs(MEMORY_DIR, exist_ok=True)
os.makedirs(OUTPUT_DATA_DIR, exist_ok=True)
os.makedirs(PROGRAMS_DIR, exist_ok=True)

print("\n[QUADRIGE BACKEND] 🚀 Initialisation")
print(f"[QUADRIGE BACKEND] BASE_DIR        = {BASE_DIR}")
print(f"[QUADRIGE BACKEND] MEMORY_DIR      = {MEMORY_DIR}")
print(f"[QUADRIGE BACKEND] OUTPUT_DATA_DIR = {OUTPUT_DATA_DIR}")
print(f"[QUADRIGE BACKEND] PROGRAMS_DIR    = {PROGRAMS_DIR}\n")


def now_ts() -> str:
    return datetime.datetime.now().strftime("%Y%m%d-%H%M%S")


def safe_slug(value: str) -> str:
    if not value:
        return "unknown"
    v = value.strip()
    v = v.replace("/", "_").replace("\\", "_")
    v = re.sub(r"\s+", "_", v)
    v = re.sub(r"[^A-Za-z0-9_\-\.]+", "_", v)
    return v


def cleanup_old_dirs(base_dir: str, keep: int = 3) -> None:
    if not os.path.exists(base_dir):
        return

    dirs = [
        os.path.join(base_dir, d)
        for d in os.listdir(base_dir)
        if os.path.isdir(os.path.join(base_dir, d))
    ]
    dirs.sort(key=lambda d: os.path.getmtime(d), reverse=True)

    for d in dirs[keep:]:
        try:
            shutil.rmtree(d)
            print(f"[QUADRIGE] 🧹 Dossier supprimé : {d}")
        except Exception as e:
            print(f"[QUADRIGE] ⚠️ Erreur suppression {d}: {e}")


def create_extraction_dir() -> Tuple[str, str]:
    extraction_id = str(uuid.uuid4())
    path = os.path.join(OUTPUT_DATA_DIR, extraction_id)
    os.makedirs(path, exist_ok=True)
    return extraction_id, path


def create_programs_dir(monitoring_location: str) -> Tuple[str, str]:
    ts = now_ts()
    ml = safe_slug(monitoring_location)
    dirname = f"programmes_{ml}_{ts}"
    path = os.path.join(PROGRAMS_DIR, dirname)
    os.makedirs(path, exist_ok=True)

    # lors de la création du dossier programmes
    meta = {
        "monitoringLocation": monitoring_location,
        "timestamp": ts,
    }
    with open(os.path.join(path, "meta.json"), "w", encoding="utf-8") as f:

        json.dump(meta, f)

    return dirname, path


def sauvegarder_filtre(program_filter: dict) -> None:
    os.makedirs(MEMORY_DIR, exist_ok=True)
    with open(LAST_FILTER_FILE, "w", encoding="utf-8") as f:
        json.dump(program_filter, f)
    print(f"[QUADRIGE BACKEND] 💾 Filtre sauvegardé dans {LAST_FILTER_FILE}")


def charger_filtre() -> dict:
    if os.path.exists(LAST_FILTER_FILE):
        with open(LAST_FILTER_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def nettoyer_csv(input_path, output_path, monitoring_location_prefix: str):
    import pandas as pd

    df = pd.read_csv(input_path, sep=";", dtype=str)

    colonnes_requises = [
        "Lieu : Mnémonique",
        "Programme : Code",
        "Programme : Libellé",
        "Programme : Etat",
        "Programme : Date de création",
        "Programme : Droit : Personne : Responsable : NOM Prénom : Liste",
    ]

    for col in colonnes_requises:
        if col not in df.columns:
            raise ValueError(f"❌ Colonne manquante dans le CSV extrait : {col}")

    df_filtre = df[df["Lieu : Mnémonique"].str.startswith(monitoring_location_prefix, na=False)]
    df_reduit = df_filtre[colonnes_requises]
    df_unique = df_reduit.drop_duplicates(subset=["Programme : Code"])

    df_unique.to_csv(output_path, sep=";", index=False)
    print(f"[QUADRIGE BACKEND] 🧹 CSV filtré enregistré : {output_path}")


def csv_to_programmes_json(csv_path: str):
    import pandas as pd

    if not os.path.exists(csv_path):
        return []

    df = pd.read_csv(csv_path, sep=";", dtype=str).fillna("")
    programmes = []
    for _, row in df.iterrows():
        programmes.append(
            {
                "name": row.get("Programme : Code", ""),
                "checked": False,
                "libelle": row.get("Programme : Libellé", ""),
                "etat": row.get("Programme : Etat", ""),
                "startDate": row.get("Programme : Date de création", ""),
                "responsable": row.get(
                    "Programme : Droit : Personne : Responsable : NOM Prénom : Liste",
                    "",
                ).replace("|", ", "),
            }
        )
    return programmes
