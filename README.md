# gn_module_quadrige

Module GeoNature permettant l’extraction de **programmes** et de **données Quadrige** via l’API GraphQL Ifremer, avec une interface utilisateur intégrée à GeoNature.

Ce module a été conçu pour :
- gérer des extractions potentiellement longues,
- rester robuste face aux erreurs partielles,
- fournir une expérience utilisateur compréhensible même en cas de résultats incomplets.

---

## 📚 Documentation

La documentation complète du module est disponible dans le dossier :

👉 https://github.com/basileandre056/gn_module_quadrige/tree/main/documentation

### Documents disponibles

- **📘 Documentation utilisateur**  
  👉 [`doc_user.md`](documentation/doc_user.md)  
  Explique le fonctionnement du module côté utilisateur (sans détails techniques).

- **🛠 Documentation technique**  
  👉 [`doc_technique.md`](documentation/doc_technique.md)  
  Destinée aux développeurs : architecture, routes, flux d’extraction, choix techniques.

- **🖥 Modifications serveur**  
  👉 [`modifications_server.md`](documentation/modifications_server.md)  
  Résume les ajustements effectués sur le serveur (Apache / Gunicorn / timeouts).

---

## ⚙️ Configuration

Actuellement, le backend utilise **uniquement** les paramètres suivants de la configuration Quadrige :

- `graphql_url`
- `access_token`

Les autres éléments (comme les localisations proposées et les champs extractibles) sont définis **côté frontend** dans le fichier :

frontend/app/constants/quadrige_constants.ts


Cela permet :
- de garder le backend générique,
- d’ajuster facilement l’UX sans modifier le serveur.

---

## 📦 Fonctionnement général

Le module fonctionne en deux grandes étapes :

1. **Extraction des programmes**
   - Filtrage par *monitoring location* (searchText)
   - Génération d’un CSV brut puis d’un CSV filtré
   - Sélection des programmes par l’utilisateur

2. **Extraction des données**
   - Lancement des extractions pour chaque programme sélectionné
   - Traitement en batch avec polling global
   - Téléchargement des fichiers générés
   - Gestion des erreurs programme par programme

---

## ⚠️ À propos des programmes sans données retournées

Lors d’une **extraction de données**, il est normal que **certains programmes ne retournent aucun fichier CSV**.  
Cela ne signifie pas nécessairement une erreur technique.

Les causes les plus fréquentes sont :

- 🔹 **Champs sélectionnés incompatibles**  
  Les champs choisis ne correspondent pas aux données disponibles pour ce programme.

- 🔹 **Période temporelle incorrecte**  
  Les dates définies dans le filtre ne couvrent aucune donnée existante.

- 🔹 **Monitoring location incohérente**  
  - Lors de l’extraction des programmes, le `searchText` peut accepter des formats ambigus  
    (ex. `XXX-126` au lieu de `126-XXX`)
  - Le programme est alors bien extrait, mais sa localisation réelle ne correspond pas
  - Lors de l’extraction des données, la *monitoring location corrigée* est appliquée  
    → aucune donnée n’est trouvée, et aucun CSV n’est généré

Dans ces cas :
- le programme est marqué avec un statut **WARNING** ou **ERROR**,
- les autres programmes continuent d’être traités normalement,
- un résumé complet est renvoyé à l’utilisateur.

Ce comportement est **volontaire** et garantit la robustesse du module.

---

## ✅ Philosophie du module

- ❌ Pas d’échec global si un programme échoue
- ✅ Traitement indépendant de chaque programme
- ✅ Résultats partiels exploitables
- ✅ Transparence pour l’utilisateur
- ✅ Backend robuste face aux volumes importants

---

## 🔧 Évolutions possibles

- Parallélisation contrôlée des téléchargements
- Extraction asynchrone (task queue)
- Cache des résultats par programme
- Amélioration du retour utilisateur (progression fine)
- Intégrer les localisation les champs sugérés dans les filtres d'extraction au fichier de config


---

