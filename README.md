# gn_module_quadrige — guide & squelette (GeoNature 2.16.3)

> Objectif : créer un dépôt **gn_module_quadrige** prêt à être branché sur GeoNature **2.16.3** avec **Angular 15** (frontend) et **Flask 3.1.1 / SQLAlchemy 1.4.x / Python 3.9** (backend), plus les commandes d’installation locales.

---

## 0) Pré-requis versions
- **Node.js** : 18 LTS (≥ 18.10)
- **npm** : livré avec Node 18
- **Angular / Angular CLI** : 15.x
- **Python** : 3.9 (cohérent avec le lock fourni)
- **Flask** : 3.1.1
- **SQLAlchemy** : 1.4.x

---

## 1) Création du dépôt & arborescence
```bash
# Créer le dossier du module (côte à côte avec votre dossier GeoNature)
mkdir -p ~/dev/gn_module_quadrige && cd ~/dev/gn_module_quadrige

# Arborescence de base
mkdir -p backend/src/gn_module_quadrige/{api,models,migrations,schemas,services,tasks}
mkdir -p backend/tests
mkdir -p frontend/{app,assets/gn_module_quadrige}
mkdir -p docs

# Fichiers racine
touch README.md LICENSE .gitignore
```

Arborescence cible :
```
gn_module_quadrige/
├─ backend/
│  ├─ pyproject.toml
│  ├─ setup.cfg
│  ├─ src/gn_module_quadrige/
│  │  ├─ __init__.py
│  │  ├─ api/blueprint.py
│  │  ├─ config_schema.py
│  │  ├─ models/__init__.py
│  │  ├─ services/__init__.py
│  │  ├─ tasks/__init__.py
│  │  └─ migrations/  (branche Alembic du module)
│  └─ tests/
├─ frontend/
│  ├─ package.json
│  ├─ package-lock.json (optionnel au démarrage)
│  ├─ tsconfig.json
│  ├─ angular.json
│  ├─ app/
│  │  ├─ gnModule.module.ts
│  │  ├─ routes.ts
│  │  └─ components/QuadrigeExtractionComponent.ts
│  └─ assets/gn_module_quadrige/
└─ docs/
```

---

## 2) Backend (Flask) — packaging & entry points GeoNature

### 2.1 `backend/pyproject.toml`
```toml
[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "gn_module_quadrige"
version = "0.1.0"
description = "Module GeoNature pour l'extraction Quadrige"
readme = "../README.md"
authors = [{ name = "Votre Nom", email = "vous@example.com" }]
license = {text = "MIT"}
requires-python = ">=3.9,<3.10"
dependencies = [
  "Flask==3.1.1",
  "Flask-SQLAlchemy==3.0.5",
  "SQLAlchemy>=1.4,<2.0",
  "Marshmallow>=3.20,<4",
  "alembic>=1.13,<2",
  "geoalchemy2==0.17.1",
]

[project.entry-points."geonature.modules"]
# Entrypoints attendus par GeoNature
code = "gn_module_quadrige:MODULE_CODE"
picto = "gn_module_quadrige:MODULE_PICTO"
blueprint = "gn_module_quadrige.api.blueprint:get_blueprint"
config_schema = "gn_module_quadrige.config_schema:get_config_schema"
migrations = "gn_module_quadrige:migrations_path"
alembic_branch = "gn_module_quadrige:ALEMBIC_BRANCH"
tasks = "gn_module_quadrige.tasks:celery_tasks"

[tool.setuptools]
package-dir = {"" = "src"}
packages = {find = {where = ["src"]}}
include-package-data = true
```

### 2.2 `backend/setup.cfg` (confort)
```ini
[flake8]
max-line-length = 100
exclude = .venv,.tox,build,dist

[tool:pytest]
addopts = -q
```

### 2.3 `backend/src/gn_module_quadrige/__init__.py`
```python
from importlib import resources

MODULE_CODE = "QUADRIGE_EXTRACT"
MODULE_PICTO = None  # chemin vers un pictogramme facultatif dans assets si besoin
ALEMBIC_BRANCH = MODULE_CODE.lower()

def migrations_path():
    # Retourne un chemin utilisable par GeoNature pour les migrations du module
    return str(resources.files(__package__) / "migrations")
```

### 2.4 `backend/src/gn_module_quadrige/api/blueprint.py`
```python
from flask import Blueprint, jsonify, request

# Le blueprint du module, préfixé par /quadrige-extract par ex.

def get_blueprint(config=None):
    bp = Blueprint("quadrige_extract", __name__, url_prefix="/quadrige-extract")

    @bp.get("/health")
    def health():
        return jsonify({"status": "ok", "module": "gn_module_quadrige"})

    @bp.get("/export")
    def export():
        # TODO: implémenter la logique d'extraction
        params = request.args.to_dict()
        return jsonify({"message": "export placeholder", "params": params})

    return bp
```

### 2.5 `backend/src/gn_module_quadrige/config_schema.py`
```python
from marshmallow import Schema, fields

class QuadrigeConfigSchema(Schema):
    # Exemple de paramètres de configuration du module
    enabled = fields.Boolean(required=True, load_default=True)
    export_max_rows = fields.Integer(required=False, load_default=10000)


def get_config_schema():
    return QuadrigeConfigSchema()
```

### 2.6 Alembic (migrations du module)
```bash
# exemple d'initialisation de l'espace migrations du module
mkdir -p backend/src/gn_module_quadrige/migrations/versions
cat > backend/src/gn_module_quadrige/migrations/README.md << 'EOF'
Migrations Alembic du module QUADRIGE_EXTRACT (branche dédiée au module).
EOF
```

---

## 3) Frontend (Angular 15)

### 3.1 `frontend/package.json`
```json
{
  "name": "gn_module_quadrige",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "build": "ng build",
    "lint": "ng lint",
    "test": "ng test"
  },
  "dependencies": {
    "@angular/animations": "^15.2.0",
    "@angular/common": "^15.2.0",
    "@angular/compiler": "^15.2.0",
    "@angular/core": "^15.2.0",
    "@angular/forms": "^15.2.0",
    "@angular/platform-browser": "^15.2.0",
    "@angular/platform-browser-dynamic": "^15.2.0",
    "@angular/router": "^15.2.0"
  },
  "devDependencies": {
    "@angular/cli": "~15.2.0",
    "@angular/compiler-cli": "^15.2.0",
    "typescript": "~4.9.5"
  }
}
```

> NB : **Pas besoin** de réinstaller Leaflet, ChartJS, etc. déjà présents dans GeoNature ; vous utiliserez les **`node_modules` de GeoNature** via les alias (voir 3.4).

### 3.2 `frontend/tsconfig.json`
```json
{
  "compileOnSave": false,
  "compilerOptions": {
    "baseUrl": ".",
    "outDir": "./dist/out-tsc",
    "sourceMap": true,
    "declaration": false,
    "downlevelIteration": true,
    "experimentalDecorators": true,
    "module": "es2020",
    "moduleResolution": "node",
    "importHelpers": true,
    "target": "es2020",
    "typeRoots": ["node_modules/@types"],
    "lib": ["es2020", "dom"],
    "paths": {
      "@geonature_common/*": [
        "../geonature/frontend/src/app/GN2CommonModule/*"
      ],
      "@librairies/*": [
        "../geonature/frontend/node_modules/*"
      ]
    }
  }
}
```

> Adapter les chemins si votre arborescence diffère. Le principe : **pointer vers le GeoNature existant**.

### 3.3 `frontend/angular.json` (extrait minimal)
```json
{
  "$schema": "https://json.schemastore.org/angular-workspace",
  "version": 1,
  "projects": {
    "gn_module_quadrige": {
      "projectType": "application",
      "root": "",
      "sourceRoot": "app",
      "architect": {
        "build": {
          "builder": "@angular-devkit/build-angular:browser",
          "options": {
            "outputPath": "dist/gn_module_quadrige",
            "index": "app/index.html",
            "main": "app/main.ts",
            "polyfills": ["zone.js"],
            "tsConfig": "tsconfig.json",
            "assets": [
              "assets"
            ]
          }
        }
      }
    }
  }
}
```

### 3.4 Module Angular racine — `frontend/app/gnModule.module.ts`
```ts
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

// Réutilisation des composants cœur GeoNature
import { GN2CommonModule } from '@geonature_common/GN2Common.module';

import { routes } from './routes';
import { QuadrigeExtractionComponent } from './components/QuadrigeExtractionComponent';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    GN2CommonModule,
    RouterModule.forChild(routes)
  ],
  declarations: [QuadrigeExtractionComponent]
})
export class GnModule {}
```

### 3.5 Routes — `frontend/app/routes.ts`
```ts
import { Routes } from '@angular/router';
import { QuadrigeExtractionComponent } from './components/QuadrigeExtractionComponent';

export const routes: Routes = [
  { path: '', component: QuadrigeExtractionComponent }
];
```

### 3.6 Composant d’exemple — `frontend/app/components/QuadrigeExtractionComponent.ts`
```ts
import { Component } from '@angular/core';

@Component({
  selector: 'gn-quadrige-extraction',
  template: `
    <h2>QUADRIGE – Extraction</h2>
    <p>Démo d'intégration du MapList et d'un petit formulaire générique.</p>

    <!-- Exemple d'assets du module -->
    <img src="assets/gn_module_quadrige/logo.png" alt="logo" width="120" />

    <!-- Exemple d'utilisation MapList (liste externe non montrée ici) -->
    <pnx-map-list idName="id_releve" height="60vh"></pnx-map-list>
  `
})
export class QuadrigeExtractionComponent {}
```

> Vous pourrez brancher le **MapListService** dans un composant parent si vous gérez une liste synchronisée.

### 3.7 Assets du module
Placez vos fichiers dans `frontend/assets/gn_module_quadrige/` (ex : `logo.png`). Ces assets seront **symlinkés** vers `GeoNature/frontend/src/assets/` à l’installation du module.

---

## 4) Environnements, dépendances & commandes

### 4.1 Backend — venv Python 3.9
```bash
cd ~/dev/gn_module_quadrige/backend
python3.9 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e .

# (Optionnel) Outillage dev
pip install black isort flake8 pytest
```

### 4.2 Frontend — Node 18 + Angular 15
```bash
# Activer Node 18 LTS (>=18.10)
nvm install 18
nvm use 18

# Angular CLI 15
npm i -g @angular/cli@15

cd ~/dev/gn_module_quadrige/frontend
npm install
```

> **Important** : vous n’avez pas besoin de doubler les libs déjà présentes dans GeoNature. Utilisez les alias de `tsconfig.json` pour référencer `@geonature_common` et `@librairies`.

---

## 5) Brancher le module sur GeoNature (dev local)

1. **Installer le backend du module dans le venv de GeoNature** (le même que celui utilisé pour lancer GeoNature), pour que les entrypoints soient détectés :
   ```bash
   # Dans le venv de GeoNature (pas celui du module si distinct)
   cd ~/dev/gn_module_quadrige/backend
   source /chemin/vers/venv-geonature/bin/activate
   pip install -e .
   ```

2. **Symlink des assets** vers le frontend GeoNature :
   ```bash
   ln -sfn ~/dev/gn_module_quadrige/frontend/assets/gn_module_quadrige \
         ~/geonature/frontend/src/assets/gn_module_quadrige
   ```

3. **Réutiliser le serveur frontend de GeoNature** en dev :
   ```bash
   cd ~/geonature/frontend/
   nvm use 18
   npm run start
   # Frontend sur http://127.0.0.1:4200
   ```

4. **Navigation vers le module** : exposez votre module via une entrée de menu dans la conf GN (ou utilisez une route paresseuse selon votre intégration). Le chargement se fait via le **module Angular racine `gnModule.module.ts`**.

---

## 6) Hooks d’intégration (rappels)
- **Entry points** exposés dans `pyproject.toml` : `code`, `blueprint`, `config_schema`, `migrations`, `alembic_branch`, `tasks`.
- **GN2CommonModule** : importez `@geonature_common/GN2Common.module` pour formulaires, sélecteurs, etc.
- **MapList** : utilisez `<pnx-map-list>` et `MapListService` pour lier carte et liste.
- **Gestion erreurs HTTP** : pour gérer vous-même l’erreur et ignorer le toaster par défaut, envoyez le header `not-to-handle: true`.

---

## 7) Documentation (Sphinx)
```bash
cd docs
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt  # créez ce fichier selon vos besoins
make html
```

---

## 8) Étapes suivantes
- Ajouter vos **migrations Alembic** (schéma dédié au module).
- Exposer des **routes API** utiles à l’extraction Quadrige.
- Brancher l’**import** (si nécessaire) en suivant la mécanique `gn_imports`.
- Écrire des **tests** backend & frontend.
- Documenter le **process d’installation** et de **configuration** du module.

