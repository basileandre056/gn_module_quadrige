# Installation du module gn_module_quadrige

Ce document décrit l’installation et la désinstallation du module **gn_module_quadrige** pour GeoNature.

---

## Prérequis

- GeoNature installé et fonctionnel
- Accès administrateur au serveur
- Environnement virtuel backend GeoNature actif
- Un fork du dépôt `gn_module_quadrige`

---

## Installation complète

### 1. Récupération du module

```bash
cd ~
git clone https://github.com/<votre_fork>/gn_module_quadrige.git
cd gn_module_quadrige
git checkout main
git pull
```

---

### 2. Activation de l’environnement backend

```bash
source ~/geonature/backend/venv/bin/activate
```

---

### 3. Configuration Quadrige

Copier le fichier de configuration exemple :

```bash
cp ~/gn_module_quadrige/quadrige_config.toml.example    ~/geonature/config/quadrige_config.toml
```

⚠️ **Important :**
- Actuellement, le backend utilise uniquement :
  - `graphql_url`
  - `access_token`
- Les localisations proposées et les champs extractibles sont définis côté frontend :
  `frontend/app/constants/quadrige_constants.ts`

---

### 4. Installation du module GeoNature

```bash
geonature install-gn-module ~/gn_module_quadrige QUADRIGE
geonature db upgrade quadrige@head
```

---

### 5. Permissions

Attribuer les droits au groupe administrateur :

```bash
geonature permissions supergrant --group --nom "Grp_admin" --yes
```

---

### 6. Redémarrage des services

```bash
sudo systemctl restart geonature geonature-worker
sudo systemctl status geonature
```

---

## Désinstallation complète

### 1. Downgrade de la base de données

```bash
geonature db downgrade quadrige@base
```

---

### 2. Suppression de la configuration

```bash
rm ~/geonature/config/quadrige_config.toml
```

---

### 3. Désinstallation Python

```bash
source ~/geonature/backend/venv/bin/activate
pip uninstall gn_module_quadrige
pip uninstall gn-module-quadrige
```

---

### 4. Nettoyage frontend

```bash
cd ~/geonature/frontend/external_modules/
rm -rf quadrige
```

---

### 5. Nettoyage en base (si nécessaire)

```sql
psql -h <host_db> -U geonatadmin -d geonature2db_prod
DELETE FROM gn_commons.t_modules WHERE module_path = 'quadrige';
\q
```

---

## Remarques importantes

- Les extractions volumineuses peuvent être longues.
- Les timeouts serveur doivent être adaptés (Gunicorn recommandé ≥ 600s).
- Certains programmes peuvent ne retourner aucune donnée (champs, dates ou monitoringLocation non compatibles).

---

✅ Installation terminée.
