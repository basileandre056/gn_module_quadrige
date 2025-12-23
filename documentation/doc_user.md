# Module Quadrige — Guide utilisateur

## 🎯 Objectif du module

Le module **Quadrige** permet d’extraire simplement des **programmes** et des **données associées** depuis la base Quadrige (Ifremer), directement depuis GeoNature, sans manipulation technique.

Il est conçu pour :
- filtrer des programmes par zone de suivi (monitoring location),
- sélectionner les programmes pertinents,
- extraire les données associées sous forme de fichiers téléchargeables,
- gérer automatiquement les volumes importants et les erreurs partielles.

---

## 🧭 Principe général

Le fonctionnement du module repose sur **2 grandes étapes** :

1. **Extraction des programmes**
2. **Extraction des données à partir des programmes sélectionnés**

Chaque étape est indépendante et peut être relancée si besoin.

---

## 1️⃣ Extraction des programmes

### Ce que fait le module
- Interroge Quadrige pour récupérer tous les programmes correspondant à une zone de suivi (ex. Mayotte, Réunion, Tromelin).
- Télécharge un fichier brut fourni par Quadrige.
- Filtre automatiquement les programmes selon la zone choisie.
- Génère :
  - un fichier CSV brut,
  - un fichier CSV filtré,
  - une liste de programmes affichée à l’écran.

### Résultat pour l’utilisateur
- Une **liste claire de programmes sélectionnables**.
- Des **fichiers CSV téléchargeables**.
- Le filtre utilisé est mémorisé pour la suite.

---


## 2️⃣ Extraction des données

### Ce que fait le module
- L’utilisateur sélectionne un ou plusieurs programmes.
- Le module lance une extraction de données **pour chaque programme**.
- Les extractions sont traitées en parallèle côté Quadrige.
- Le module surveille l’avancement global.

### Gestion des volumes importants
- Si un programme échoue, **les autres continuent**.
- Les erreurs sont isolées par programme.
- Les extractions longues sont automatiquement gérées (pas de blocage global).

### Résultat pour l’utilisateur
- Un ou plusieurs fichiers ZIP téléchargeables.
- Un résumé indiquant :
  - les extractions réussies,
  - les avertissements (aucune donnée),
  - les erreurs éventuelles.

---

## ⚠️ Gestion des erreurs

Le module est conçu pour être **robuste** :
- Une erreur sur un programme n’annule pas toute l’extraction.
- Les avertissements sont signalés clairement.
- Les erreurs sont expliquées sans bloquer l’interface.

---

## 🗂️ Gestion automatique des fichiers

- Les fichiers sont stockés temporairement sur le serveur.
- Les anciennes extractions sont automatiquement nettoyées.
- Seules les dernières extractions sont conservées.

Aucune action manuelle n’est requise.

---

## ✅ Avantages pour l’utilisateur

- Pas de connaissances techniques nécessaires.
- Interface guidée et progressive.
- Gestion des gros volumes de données.
- Téléchargement direct des résultats.
- Sécurité et stabilité des extractions.

---

## 🧩 En résumé

Le module Quadrige permet de :
- explorer facilement les programmes disponibles,
- extraire les données associées en toute sécurité,
- gérer des volumes importants sans risque,
- travailler efficacement depuis GeoNature.

---

📌 *Pour toute question ou évolution, le module est conçu pour être extensible et améliorable sans modifier son usage.*
