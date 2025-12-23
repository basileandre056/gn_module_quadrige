# Modifications serveur – GeoNature / Module Quadrige

## Contexte

Lors de l’utilisation du module **Quadrige** dans GeoNature, des erreurs  
**500 – Internal Server Error** survenaient lors :

- de l’extraction de programmes volumineux (ex : La Réunion, Mayotte)
- de l’extraction de données associées à un grand nombre de programmes

Les extractions de faible volume (ex : Tromelin – 3 programmes) fonctionnaient correctement.

---

## Diagnostic

### Symptômes observés

- Réponse HTTP **500** côté navigateur
- Header `Server: Apache/2.4.x`
- Connexion fermée brutalement (`Connection: close`)
- Absence d’erreur explicite dans le frontend
- Aucune erreur fonctionnelle dans le code Python (tests GraphQL unitaires OK)

### Cause identifiée

Le **timeout Gunicorn** était configuré à **30 secondes**, ce qui est insuffisant pour :

- les appels GraphQL `executeProgramExtraction`
- le polling `getExtraction`
- le téléchargement des fichiers CSV / ZIP
- les traitements CSV côté backend

➡️ Les workers Gunicorn étaient **tués avant la fin du traitement**, provoquant :
- une coupure de connexion
- un `500 Internal Server Error` renvoyé par Apache (reverse proxy)

---

## Modifications apportées

### 1️⃣ Service systemd GeoNature

Fichier modifié :

```
/etc/systemd/system/geonature.service
```

#### Avant
```ini
Environment=GUNICORN_TIMEOUT=30
TimeoutStartSec=10
TimeoutStopSec=5
```

#### Après
```ini
Environment=GUNICORN_TIMEOUT=600
TimeoutStartSec=30
TimeoutStopSec=60
```

➡️ Permet aux workers Gunicorn de rester actifs jusqu’à **10 minutes**.

---

### 2️⃣ Redémarrage des services

Commandes exécutées :

```bash
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl restart geonature geonature-worker
```

Vérification :

```bash
ps aux | grep geonature | grep gunicorn
```

Résultat attendu :
```text
--timeout=600
```

---

### 3️⃣ Apache (reverse proxy)

Aucune modification supplémentaire nécessaire côté Apache.

Configuration existante (extrait) :

```apache
ProxyPass / http://127.0.0.1:8080/
ProxyPassReverse / http://127.0.0.1:8080/
```

Apache fonctionne correctement tant que Gunicorn ne coupe pas la connexion.

---

## Résultat après correction

### ✅ Program extraction
- Extraction avec **peu de programmes** : OK
- Extraction avec **beaucoup de programmes (80+)** : OK
- Temps de réponse long mais stable
- Réponses HTTP **200**

### ✅ Data extraction
- Polling long autorisé
- Téléchargement ZIP fonctionnel
- Gestion correcte des statuts `SUCCESS` et `WARNING`
- Réponses HTTP **200**

-Il subsiste encore quelques difficultés : l’extraction des 87 programmes de la Réunion est trop lourde et échoue, tandis que les extractions de plus d’une dizaine de programmes fonctionnent correctement. La suite consistera donc à chercher des pistes d’optimisation du code.

### ✅ UX
- Plus d’erreur 500
- Messages applicatifs corrects
- Pas de coupure réseau côté navigateur

---

## Conclusion

- Le problème n’était **ni fonctionnel, ni GraphQL, ni frontend**
- Il s’agissait d’un **timeout Gunicorn trop court**
- L’augmentation du timeout à **600s** a résolu le problème de manière fiable

Le module **Quadrige** est désormais **opérationnel pour des extractions lourdes**.

---

