# backend/gn_module_quadrige/utils_backend.py
import os
import json
import datetime
import tempfile
import requests

# -------------------------
# Dossiers de travail (dans /tmp pour un module externe)
# -------------------------

BASE_DIR = os.path.join(tempfile.gettempdir(), "quadrige_module")
MEMORY_DIR = os.path.join(BASE_DIR, "memory")
OUTPUT_DATA_DIR = os.path.join(BASE_DIR, "output_data")
LAST_FILTER_FILE = os.path.join(MEMORY_DIR, "last_filter.json")

os.makedirs(MEMORY_DIR, exist_ok=True)
os.makedirs(OUTPUT_DATA_DIR, exist_ok=True)

print("\n[QUADRIGE BACKEND] 🚀 Initialisation")
print(f"[QUADRIGE BACKEND] BASE_DIR        = {BASE_DIR}")
print(f"[QUADRIGE BACKEND] MEMORY_DIR      = {MEMORY_DIR}")
print(f"[QUADRIGE BACKEND] OUTPUT_DATA_DIR = {OUTPUT_DATA_DIR}\n")


def get_output_path(filename):
    return os.path.join(OUTPUT_DATA_DIR, filename)


def nettoyer_dossier_memory() -> None:
    """
    Supprime tous les anciens fichiers programmes dans MEMORY_DIR,
    sauf le fichier de filtre JSON (last_filter.json).
    """
    try:
        for fichier in os.listdir(MEMORY_DIR):
            chemin = os.path.join(MEMORY_DIR, fichier)
            if fichier != "last_filter.json" and os.path.isfile(chemin):
                os.remove(chemin)
                print(f"[QUADRIGE BACKEND] 🧹 Fichier supprimé : {fichier}")
    except Exception as e:
        print(f"[QUADRIGE BACKEND] ⚠️ Erreur nettoyage MEMORY_DIR : {e}")


def nettoyer_output_data() -> None:
    """
    Supprime tous les fichiers du dossier OUTPUT_DATA_DIR
    avant une nouvelle extraction.
    """
    try:
        for f in os.listdir(OUTPUT_DATA_DIR):
            path = os.path.join(OUTPUT_DATA_DIR, f)
            if os.path.isfile(path):
                os.remove(path)
                print(f"[QUADRIGE BACKEND] 🧹 Fichier supprimé : {f}")
    except Exception as e:
        print(f"[QUADRIGE BACKEND] ⚠️ Erreur nettoyage OUTPUT_DATA_DIR : {e}")


def name_extraction_data(programmes, download_links, filter_data, monitoring_location):
    """
    Télécharge et renomme les fichiers ZIP d'extraction de données.
    Format : <programme_code>_<monitoring_location>_<filter_name>_<date>.zip

    Retourne une liste de dict :
    [
      {"file_name": "...", "url": "http://.../output_data/xxx.zip"},
      ...
    ]
    """
    os.makedirs(OUTPUT_DATA_DIR, exist_ok=True)

    filter_name = filter_data.get("name", "filtre").replace(" ", "_")
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

    renamed_files = []

    for prog, url in zip(programmes, download_links):
        try:
            filename = f"{prog}_{monitoring_location}_{filter_name}_{timestamp}.zip"
            safe_filename = filename.replace("/", "_").replace("\\", "_")
            file_path = os.path.join(OUTPUT_DATA_DIR, safe_filename)

            r = requests.get(url)
            r.raise_for_status()
            with open(file_path, "wb") as f:
                f.write(r.content)

            renamed_files.append(
                {
                    "file_name": safe_filename,
                    # ⚠️ l’URL finale sera /quadrige/output_data/...
                    "url": f"/quadrige/output_data/{safe_filename}",
                }
            )
            print(f"[QUADRIGE BACKEND] 💾 Fichier sauvegardé : {safe_filename}")

        except Exception as e:
            print(f"[QUADRIGE BACKEND] ⚠️ Erreur téléchargement {prog}: {e}")

    return renamed_files


def sauvegarder_filtre(program_filter: dict) -> None:
    """
    Sauvegarde le filtre utilisé pour l’extraction des programmes.
    """
    os.makedirs(MEMORY_DIR, exist_ok=True)
    with open(LAST_FILTER_FILE, "w", encoding="utf-8") as f:
        json.dump(program_filter, f)
    print(f"[QUADRIGE BACKEND] 💾 Filtre sauvegardé dans {LAST_FILTER_FILE}")


def charger_filtre() -> dict:
    """
    Recharge le dernier filtre utilisé (sinon renvoie {}).
    """
    if os.path.exists(LAST_FILTER_FILE):
        with open(LAST_FILTER_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}
