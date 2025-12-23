# Documentation technique — Module GeoNature Quadrige

## 1. Objectif du module

Le module **gn_module_quadrige** permet à GeoNature d’interagir avec l’API GraphQL Quadrige (Ifremer) afin de :

- extraire des **programmes** selon une localisation (monitoringLocation),
- extraire des **données associées à un ou plusieurs programmes**,
- gérer des volumes importants de données de manière robuste (batch, polling global, tolérance aux erreurs).

Le module est conçu pour :
- éviter les timeouts HTTP,
- ne pas bloquer une extraction complète si un programme échoue,
- fournir un résumé exploitable côté frontend.

---

## 2. Configuration utilisée

### 2.1 Configuration backend (GeoNature)

Le backend utilise **uniquement** les paramètres suivants de la configuration Quadrige :

- `graphql_url`
- `access_token`

Ces paramètres sont lus via :

```python
from geonature.utils.config import config as gn_config
cfg = gn_config["QUADRIGE"]
```

⚠️ **Les autres champs éventuels du fichier TOML (localisations, champs extractables, etc.) ne sont actuellement pas utilisés par le backend.**

---

### 2.2 Configuration frontend

Les éléments suivants sont **définis côté frontend** :

- les **localisations proposées** à l’utilisateur,
- les **champs extractibles** (mesures, métadonnées, etc.).

Ils se trouvent dans :

```
frontend/app/constants/quadrige_constants.ts
```

Le backend se contente de **consommer les choix faits par le frontend**.

---

## 3. Architecture générale

```
Frontend Angular
   │
   ▼
Routes Flask (routes.py)
   │
   ├── extraction_programs.py   → extraction des programmes
   ├── extraction_data.py       → extraction des données (batch)
   ├── build_query.py           → construction des requêtes GraphQL
   └── utils_backend.py         → utilitaires (fichiers, CSV, mémoire)
```

---

## 4. routes.py — Points d’entrée API

### 4.1 `/program-extraction` (POST)

**Rôle** :
- lancer une extraction de programmes Quadrige,
- télécharger le CSV généré,
- filtrer localement les programmes par localisation,
- retourner la liste des programmes exploitables.

**Étapes principales** :
1. Validation du `monitoringLocation`.
2. Appel à `extract_programs()`.
3. Téléchargement du CSV brut.
4. Nettoyage du CSV (`nettoyer_csv`).
5. Conversion en JSON pour le frontend.

---

### 4.2 `/data-extractions` (POST)

**Rôle** :
- extraire les données pour une liste de programmes sélectionnés,
- gérer les extractions en batch avec polling global,
- tolérer les erreurs individuelles.

**Comportement clé** :
- un programme en erreur **n’annule pas** les autres,
- chaque programme retourne un statut (`SUCCESS`, `WARNING`, `ERROR`).

---

### 4.3 `/last-programmes` (GET)

Permet au frontend de :
- retrouver la dernière extraction de programmes,
- restaurer l’état après rechargement de la page.

---

### 4.4 `/filtrage_seul` (POST)

Permet de :
- relancer uniquement le filtrage local du CSV,
- sans réinterroger Quadrige.

---

## 5. extraction_programs.py — Extraction des programmes

### Principe

- Une **seule extraction distante** est lancée via `executeProgramExtraction`.
- Un **polling adaptatif** vérifie l’état de la tâche.
- Le backend attend la disponibilité du fichier CSV.

### Points importants

- Timeout progressif (backoff simple).
- Une seule tâche Quadrige, quel que soit le nombre de programmes.

---

## 6. extraction_data.py — Extraction des données (batch)

### 6.1 Phase 1 — Lancement des jobs

- Une extraction Quadrige est lancée **par programme**.
- Les `job_id` sont stockés en mémoire.

### 6.2 Phase 2 — Polling global

- Un polling unique vérifie l’état de tous les jobs.
- Les programmes terminés sont retirés du lot restant.
- En cas d’erreur ou de timeout :
  - le programme est marqué `ERROR`,
  - les autres continuent.

### 6.3 Phase 3 — Téléchargement

- Les fichiers sont téléchargés uniquement pour les statuts valides.
- Téléchargement en streaming pour limiter la mémoire.

---

## 7. build_query.py — Construction GraphQL

Responsabilités :
- validation minimale des filtres,
- génération dynamique de la requête GraphQL `executeResultExtraction`.

Ce fichier est volontairement simple afin de :
- faciliter l’évolution du schéma GraphQL,
- centraliser la logique de requêtage.

---

## 8. utils_backend.py — Utilitaires

Fonctionnalités principales :

- gestion des répertoires temporaires,
- nettoyage automatique des anciennes extractions,
- filtrage CSV local (Pandas),
- conversion CSV → JSON frontend.

⚠️ Les traitements lourds (CSV) sont réalisés **après** les appels réseau pour éviter des timeouts.

---

## 9. Choix techniques clés

- ✔️ Polling global plutôt que séquentiel
- ✔️ Tolérance aux erreurs par programme
- ✔️ Streaming des fichiers volumineux
- ✔️ Séparation claire frontend / backend
- ✔️ Backend agnostique des règles métier

---

## 10. Pistes d’évolution

- Passage à un traitement asynchrone (Celery / RQ)
- Stockage des métadonnées d’extraction en base
- Endpoint de suivi de progression
- Mutualisation de certaines requêtes GraphQL

---



