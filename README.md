
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
   - Mot de passe : *(fourni séparément)*

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
- Chemin d'installation (souvent) :  
  `/home/geonatureadmin/geonature2`

---

## 🟦 3. Connexion SSH depuis la VM Windows

Dans la session PowerShell Guacamole :

```powershell
ssh geonatureadmin@IP_DU_SERVEUR
```

Résultat attendu :

```bash
geonatureadmin@geonature:~$
```

---

## 🟦 4. Vérifications du serveur GeoNature

### 4.1 Vérifier les services

```bash
sudo systemctl status geonature
sudo systemctl status geonature-web
sudo systemctl status geonature-workers
```

### 4.2 Vérifier l’arborescence attendue

```bash
ls /home/
ls /home/geonatureadmin/
ls /home/geonatureadmin/geonature2/
ls /home/geonatureadmin/geonature2/venv/
```

### 4.3 Vérifier Python / pip

```bash
source /home/geonatureadmin/geonature2/venv/bin/activate
python3 --version
pip --version
```

---

## 🟦 5. Vérifications du module Quadrige AVANT installation

### 5.1 Vérifier la structure du projet

```text
gn_module_quadrige/
  backend/
    gn_module_quadrige/
      __init__.py
      routes.py
      blueprint.py
      config_schema_toml.py
      extraction_data.py
      extraction_programs.py
      utils_backend.py
      migrations/
  frontend/
    angular.json
    app/
  VERSION
  README.rst
  setup.py
  requirements_backend.txt
```

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
[quadrige]
graphql_url = "https://quadrige-core.ifremer.fr/graphql/public"
access_token = "TOKEN_PRODUCTION"
```

(Le vrai token sera renseigné sur le serveur de prod.)

---

# 🟦 6. Installation du module Quadrige sur le serveur GeoNature

Cette partie a été **mise à jour pour intégrer les étapes obligatoires issues de la documentation officielle GeoNature**.

## 6.1 Télécharger le module
```bash
cd /home/geonatureadmin/modules
git clone https://github.com/basileandre056/gn_module_quadrige.git
```

---

## 6.2 Installation du backend (méthode officielle : mode éditable)

> ⚠ Le mode *editable* est recommandé par l’équipe GeoNature pour faciliter les mises à jour et les correctifs.

```bash
source ~/geonature2/venv/bin/activate
pip install --editable /home/geonatureadmin/modules/gn_module_quadrige
sudo systemctl restart geonature
```

---

## 6.3 Installation du frontend (méthode officielle)

### 6.3.1 Créer le lien symbolique

GeoNature utilise `frontend/external_modules` pour intégrer les modules Angular.

```bash
cd ~/geonature2/frontend/external_modules/
ln -s /home/geonatureadmin/modules/gn_module_quadrige/frontend quadrige
```

*(Le nom du lien doit être le **code du module en minuscule** : `quadrige`)*

### 6.3.2 Rebuild du frontend global
```bash
cd ~/geonature2/frontend/
nvm use
npm run build
```

---

## 6.4 Installation de la base de données du module

Si le module intègre un schéma, migrations ou tables spécifiques :

```bash
source ~/geonature2/venv/bin/activate
geonature upgrade-modules-db quadrige
```

---

## 6.5 Configuration du module via GeoNature

Créer :
```bash
nano ~/geonature2/config/quadrige_config.toml
```

Contenu :
```toml
[quadrige]
graphql_url = "https://quadrige-core.ifremer.fr/graphql/public"
access_token = "TOKEN_DE_PRODUCTION"
```

### Rechargement automatique (GeoNature ≥ 2.12)
```bash
sudo systemctl daemon-reload
sudo systemctl restart geonature
```

### Anciennes versions (< 2.12)
```bash
sudo systemctl reload geonature
```

---

# 🟦 7. Redémarrer GeoNature
```bash
sudo systemctl restart geonature
sudo systemctl restart geonature-web
sudo systemctl restart geonature-workers
```

---

# 🟦 8. Vérification du chargement du module

### API backend
```bash
curl http://localhost/api/quadrige/last-programmes
```

### Frontend
`https://VOTRE_SERVEUR/quadrige`

---

## 🟦 9. Vérification du chargement du module

### 9.1 Tester l’API backend

Depuis le serveur :

```bash
curl http://localhost/api/quadrige/last-programmes
```

Résultat attendu :
- une réponse JSON (même vide),
- **pas** d’erreur 500 Flask/Apache.

### 9.2 Tester le frontend

Dans un navigateur :

```text
https://VOTRE_SERVEUR/quadrige
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

---

## 🟦 11. Checklist à valider

| Tâche                                 | Statut |
|--------------------------------------|--------|
| Accès Guacamole OK                   | ⬜ |
| Accès SSH au serveur GeoNature OK    | ⬜ |
| GeoNature installé et accessible     | ⬜ |
| Module Quadrige cloné                | ⬜ |
| Module Quadrige installé (pip)       | ⬜ |
| Module activé dans geonature_config  | ⬜ |
| TOML module créé                     | ⬜ |
| Frontend GeoNature rebuild           | ⬜ |
| Services redémarrés                  | ⬜ |
| API du module accessible             | ⬜ |
| Extraction simple OK                 | ⬜ |
| Extraction multiple OK               | ⬜ |

---

## Vérifications rapides

### Tester que la configuration est chargée

```text
https://votre-geonature/api/quadrige/debug_config
```

### Accéder au frontend

```text
https://votre-geonature/quadrige
```

---

## Contact & Support

Pour toute question technique ou demande d'amélioration, contacter le mainteneur du module.
