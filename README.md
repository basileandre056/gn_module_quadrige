
# Module GeoNature Quadrige — Guide d'installation

## Présentation

Le module **Quadrige** permet d'interfacer GeoNature avec l'API GraphQL d'Ifremer afin d'extraire :
- la liste des programmes,  
- les données associées,  
- et les fichiers ZIP générés par Quadrige Core.  

Le module propose :
- un **backend Python/Flask** intégré à GeoNature  
- un **frontend Angular** intégré automatiquement via le module GeoNature  

---

# TO_DO.md — Préparation complète avant déploiement du module Quadrige

## 🟦 1. Accès au bastion via Apache Guacamole

**Guacamole** permet d’accéder à une VM Windows interne, depuis laquelle on se connecte en SSH au serveur GeoNature.

### Étapes :
1. Ouvrir un navigateur.  
2. Désactiver le proxy (important).  
3. Accéder à :

   `https://165.169.200.105/guacamole/`

4. Se connecter :
   - Login : `rbouilly`
   - Mot de passe : ...

Résultat attendu :  
Connexion à Apache Guacamole.

---

## 🟦 2. Comprendre les flux d’accès

- Guacamole → VM Windows  
- VM Windows → SSH vers le serveur GeoNature

### Infos nécessaires :
- IP du serveur GeoNature  
- Identifiants SSH  
- Port SSH éventuel  


---


## 🟦 4. Vérifications du serveur GeoNature

### 4.1 Vérifier les services

```bash
sudo systemctl status geonature
sudo systemctl status geonature-web
sudo systemctl status geonature-workers
```

---

## 🟦 5. Vérifications du module Quadrige AVANT installation

### 5.1 Vérifier la structure du projet


✔ Structure compatible avec GeoNature  
✔ `MODULE_CODE = "quadrige"`  
✔ Entrypoints définis dans `setup.py`

### 5.2 Vérifier que le TOML d’exemple existe (local)

Dans le dépôt local :

```text
gn_module_quadrige/module_code_config.toml
```

Contenu attendu :

```toml
# -------- CONFIG FRONTEND -------
MODULE_CODE = "QUADRIGE"
MODULE_URL  = "/quadrige"
TITLE_MODULE = "Module Quadrige"
DESCRIPTION_MODULE = "Extraction Quadrige – Ifremer"
ICON = "assets/quadrige/picto.png"

[PERMISSION_LEVEL]
module = "QUADRIGE_MODULES"

# -------- CONFIG BACKEND -------
graphql_url = "https://quadrige-core.ifremer.fr/graphql/public"
access_token="2L7BiaziVfbd9iLhhhaq6MiWRKGwJrexUmR183GgiJx4:96A2A2AEDE6115BE9C462247461D26B317CD1602D73AE47408EDA70A04DCF21A:1|mhQMC3j5nad54G615G7NotJILcTeQv9KKbr8Fj+pn6Sk2T+pY3xIdNikUzIuJ3T43FeNKBYAlKnQNWpvhdKWBg=="
# Lieux Ifremer
locations = [
  { code = "126-", label = "Réunion" },
  { code = "145-", label = "Mayotte" },
  { code = "048-", label = "Maurice" },
  { code = "153-", label = "Île Tromelin" },
  { code = "152-", label = "Îles Glorieuses" },
  { code = "154-", label = "Île Juan de Nova" },
  { code = "155-", label = "Île Bassas da India" },
  { code = "156-", label = "Île Europa" }
]

# Champs d'extraction
extractable_fields = [
  "MEASUREMENT_COMMENT",
  "MEASUREMENT_PMFMU_METHOD_NAME",
  "MEASUREMENT_NUMERICAL_VALUE",
  "MEASUREMENT_PMFMU_PARAMETER_NAME",
  "MEASUREMENT_REFERENCE_TAXON_NAME",
  "MEASUREMENT_REFERENCE_TAXON_TAXREF",
  "MEASUREMENT_STRATEGIES_NAME",
  "MEASUREMENT_UNDER_MORATORIUM",
  "MEASUREMENT_PMFMU_UNIT_SYMBOL",
  "MONITORING_LOCATION_BATHYMETRY",
  "MONITORING_LOCATION_CENTROID_LATITUDE",
  "MONITORING_LOCATION_CENTROID_LONGITUDE",
  "MONITORING_LOCATION_ID",
  "MONITORING_LOCATION_LABEL",
  "MONITORING_LOCATION_NAME",
  "SAMPLE_LABEL",
  "SAMPLE_MATRIX_NAME",
  "SAMPLE_SIZE",
  "SAMPLE_TAXON_NAME",
  "SURVEY_COMMENT",
  "SURVEY_DATE",
  "SURVEY_LABEL",
  "SURVEY_NB_INDIVIDUALS",
  "SURVEY_OBSERVER_DEPARTMENT_ID",
  "SURVEY_OBSERVER_DEPARTMENT_LABEL",
  "SURVEY_OBSERVER_DEPARTMENT_NAME",
  "SURVEY_OBSERVER_DEPARTMENT_SANDRE",
  "SURVEY_OBSERVER_ID",
  "SURVEY_OBSERVER_NAME",
  "SURVEY_PROGRAMS_NAME",
  "SURVEY_RECORDER_DEPARTMENT_ID",
  "SURVEY_RECORDER_DEPARTMENT_LABEL",
  "SURVEY_RECORDER_DEPARTMENT_NAME",
  "SURVEY_RECORDER_DEPARTMENT_SANDRE",
  "SURVEY_TIME",
  "SURVEY_UNDER_MORATORIUM"
]

```
---

# 🟦 6. Installation du module Quadrige sur le serveur GeoNature

## 6.1 Télécharger le module
```bash
cd ~/geonature
git clone https://github.com/basileandre056/gn_module_quadrige.git
cd gn_module_quadrige
git checkout rdv_equipe_geonature

```
## 6.2 Installation GLOBALE

Installation globale 

```bash
source ~/geonature/backend/venv/bin/activate

geonature install-gn-module ~/gn_module_quadrige QUADRIGE


```


## 6.3 Installation de la base de données du module

```bash

Si le module intègre un schéma, migrations ou tables spécifiques :

```bash
source ~/geonature2/venv/bin/activate
geonature upgrade-modules-db quadrige
```

---

## 6.5 Configuration du module via GeoNature

```bash
cp ~/gn_module_quadrige/quadrige_config.toml.example ~/geonature/config/quadrige_config.toml

```
pour l'éditer :
```bash
nano ~/geonature2/config/quadrige_config.toml
```
puis 
### Rechargement automatique (GeoNature ≥ 2.12)
```bash
sudo systemctl restart geonature geonature-worker
sudo systemctl status geonature
```

### Anciennes versions (< 2.12)
```bash
sudo systemctl reload geonature
```

---

## 🟦 9. Vérification du chargement du module

### 9.1 Tester l’API backend

Depuis le serveur :

```bash
curl http://10.172.2.156/geonature/api/quadrige/config

Résultat attendu :
- une réponse JSON avec la config chargée et exposée par GeoNature,
- **pas** d’erreur 500 Flask/Apache.

### 9.2 Tester le frontend

Dans un navigateur :

```text
http://10.172.2.156/geonature/#/quadrige
```

Le frontend du module Quadrige doit s’afficher (liste des programmes, filtres, etc.).

---

## 🟦 10. Tests des extractions Quadrige

### 10.1 Extraction d’un programme (exemple)

```bash
curl -X POST http://localhost/api/quadrige/data-extractions   -H "Content-Type: application/json"   -d '{
        "programmes": [
          "ORC_MAYOTTE_BELT_POISSONS"
        ],
        "filter": {
          "name": "test_deploy",
          "fields": ["MONITORING_LOCATION_NAME"]
        }
      }'
```

### 10.2 Extraction de plusieurs programmes

```bash
curl -X POST http://localhost/api/quadrige/data-extractions   -H "Content-Type: application/json"   -d '{
        "programmes": [
          "ORC_MAYOTTE_BELT_POISSONS",
          "ORC_MAYOTTE_LIT_BENTHOS",
          "EI_MAYOTTE_BLANCHISSEMENT_PCS_BENTHOS"
        ],
        "filter": {
          "name": "test_multiple",
          "fields": ["MONITORING_LOCATION_NAME"]
        }
      }'
```

Résultat attendu :
- Plusieurs ZIP générés et sauvegardés,
- Si 1 programme échoue → les autres continuent,
- Aucun crash du backend.

