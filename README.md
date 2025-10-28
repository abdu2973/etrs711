# Gestion de Cave à Vin - Projet ETRS711

Projet réalisé pour le module **ETRS711 - Conception et Programmation Orientée Objet**.

Cette application web permet à plusieurs utilisateurs de gérer leur cave à vin personnelle. Ils peuvent créer une cave virtuelle, y ajouter des bouteilles, les organiser sur des étagères, et les noter.

## Fonctionnalités Implémentées ✅

* **Gestion de comptes utilisateurs** : Création de compte et connexion sécurisée.
* **Gestion de la cave** : Chaque utilisateur peut créer sa cave virtuelle.
* **Gestion des étagères** : Ajout et suppression d'étagères avec nom et capacité paramétrable.
* **Gestion du stock** : Ajout de bouteilles (issues d'une liste prédéfinie) sur une étagère, en respectant la capacité. Gestion des quantités pour les bouteilles identiques.
* **Retrait et Archivage** :
    * Retirer une bouteille (-1 du stock).
    * Archiver une bouteille (-1 du stock ET ajout d'une note personnelle avec commentaire).
* **Visualisation Personnelle** : Affichage de la cave avec les étagères, les bouteilles stockées (quantité, détails), et les notes personnelles de l'utilisateur.
* **Tri des bouteilles** : Tri des bouteilles dans la cave par Nom (A-Z, Z-A), Année (récent/ancien), ou Prix (cher/moins cher).
* **Notes Communautaires** :
    * Affichage d'une page dédiée avec toutes les notes et commentaires laissés par tous les utilisateurs.
    * Calcul et affichage de la **note moyenne** de la communauté pour chaque type de bouteille (visible dans la cave et sur la page des notes).
* **Interface Web** : Utilisation de Flask pour le backend, HTML/CSS pour le frontend.
* **Persistance des données** : Base de données SQLite pour stocker les informations.

## Technologies Utilisées 💻

* **Langage** : Python 3
* **Framework Web** : Flask
* **Base de Données** : SQLite
* **Frontend** : HTML, CSS
* **Conception** : UML

## Conception UML 📊

*(Note : Les diagrammes réels seraient insérés ici sous forme d'images)*

### Diagramme de Cas d'Utilisation

* **Acteur Principal** : Utilisateur (Amateur de vin)
* **Cas d'utilisation principaux** :
    * S'inscrire
    * Se connecter
    * Gérer sa cave (Voir, Créer)
    * Gérer les étagères (Ajouter, Supprimer, Voir contenu)
    * Gérer le stock de bouteilles (Ajouter, Retirer)
    * Archiver une bouteille (Noter, Commenter)
    * Voir ses notes personnelles
    * Voir les notes de la communauté
    * Trier les bouteilles de sa cave


### Diagramme de Classes

* **Classes principales** :
    * `Utilisateurs` (id\_utilisateur, nom, prenom, identifiant, mdp, voir\_cave(), voir\_notes(), ...)
    * `Bouteilles` (id\_bouteille, domaine\_viticole, nom, type, annee, region, photo, prix, ...)
    * `Etageres` (id\_Etagere, nom, capacite, id\_utilisateur, creer\_etagere(), supprimer\_etagere(), ajouter\_bouteille\_stock(), retirer\_bouteille\_stock())
    * `Cave` (id\_utilisateur, id\_etagere, cree\_cave(), associe\_etagere())
    * `Notes` (id\_utilisateur, id\_bouteille, notes, commentaires, id\_commentaires, ajouter\_note(), voir\_toutes\_les\_notes(), calculer\_note\_moyenne())
    * `Database` (conn, create\_tables(), fin\_connexion())
* **Relations principales** :
    * `Utilisateurs` 1 -- \* `Cave` (Un utilisateur a une cave)
    * `Cave` \* -- \* `Etageres` (La cave contient plusieurs étagères via la table Cave)
    * `Etageres` \* -- \* `Bouteilles` (Relation Many-to-Many via la table `StockEtagere` avec l'attribut `quantite`)
    * `Utilisateurs` \* -- \* `Notes` (Un utilisateur peut laisser plusieurs notes)
    * `Bouteilles` \* -- \* `Notes` (Une bouteille peut avoir plusieurs notes)


### Diagrammes de Séquence (Exemples)

1.  **Séquence : Ajouter une bouteille à une étagère**
    * L'utilisateur soumet le formulaire d'ajout depuis `cave.html`.
    * La route `/cave` (dans `site_html.py`) reçoit la requête POST.
    * Elle vérifie l'action ("ajouter\_bouteille").
    * Elle instancie `Etageres` et appelle `ajouter_bouteille_stock()`.
    * `ajouter_bouteille_stock()` (dans `class711.py`) :
        * Se connecte à la DB (`Cave.db`).
        * Vérifie la capacité de l'étagère (SELECT capacite FROM Etageres).
        * Calcule le stock actuel (SELECT SUM(quantite) FROM StockEtagere).
        * Compare stock + ajout vs capacité.
        * Si OK, vérifie si la bouteille existe déjà (SELECT quantite FROM StockEtagere).
        * Effectue un INSERT ou un UPDATE dans `StockEtagere`.
        * Commit la transaction.
        * Retourne succès/échec à `site_html.py`.
    * `site_html.py` ajoute un message Flash et redirige vers `/cave`.


2.  **Séquence : Archiver une bouteille**
    * L'utilisateur soumet le formulaire d'archivage depuis `cave.html`.
    * La route `/cave` reçoit la requête POST.
    * Elle vérifie l'action ("archiver\_bouteille").
    * Elle instancie `Etageres` et appelle `retirer_bouteille_stock()`.
    * `retirer_bouteille_stock()` (dans `class711.py`) :
        * Se connecte à la DB.
        * Vérifie le stock actuel de la bouteille (SELECT quantite).
        * Si stock > 0, effectue un UPDATE (quantite - 1) ou DELETE si quantite == 1 dans `StockEtagere`.
        * Commit la transaction.
        * Retourne succès/échec à `site_html.py`.
    * Si le retrait a réussi :
        * `site_html.py` instancie `Notes` avec les infos du formulaire.
        * Appelle `ajouter_note()`.
        * `ajouter_note()` (dans `class711.py`) :
            * Se connecte à la DB.
            * Effectue un INSERT dans la table `Notes`.
            * Commit la transaction.
            * Retourne succès/échec à `site_html.py`.
    * `site_html.py` ajoute les messages Flash appropriés et redirige vers `/cave`.
