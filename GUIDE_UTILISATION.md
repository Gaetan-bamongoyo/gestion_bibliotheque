# Guide d’utilisation de l’application : Gestion de Bibliothèque

## 1. Introduction
### Présentation de l’application
Cette application est une solution moderne et intuitive conçue pour automatiser les processus de gestion d'une bibliothèque. Elle permet de suivre efficacement les stocks de livres, les inscriptions des lecteurs, ainsi que le cycle complet des emprunts et des retours.

### Objectif
L'objectif principal est de simplifier le travail des gestionnaires de bibliothèque en offrant une visibilité en temps réel sur la disponibilité des ouvrages, en automatisant le calcul des pénalités de retard et en fournissant des statistiques détaillées sur l'activité de l'établissement.

---

## 2. Fonctionnalités principales
L'application s'articule autour de quatre axes majeurs :

*   **Gestion du Catalogue** : Organisation des livres par catégories, suivi des quantités totales et disponibles, et recherche rapide par titre, auteur ou ISBN.
*   **Gestion des Lecteurs** : Enregistrement des membres, suivi de leur historique d'emprunts et contrôle de leur éligibilité (limite d'emprunts en cours).
*   **Gestion des Flux (Emprunts/Retours)** : Processus simplifié pour prêter un livre, suivi automatique des retards et gestion des retours avec calcul de pénalités.
*   **Pilotage et Analyse** : Tableau de bord dynamique, historique complet des transactions et statistiques visuelles (livres les plus lus, catégories populaires, etc.).

---

## 3. Accès à l’application
L'accès est sécurisé et différencié selon le rôle de l'utilisateur (Administrateur ou Gestionnaire).

### Connexion
1.  Rendez-vous sur la page de connexion de l'application.
2.  Saisissez votre **Nom d'utilisateur** et votre **Mot de passe**.
3.  Cliquez sur **"Se connecter"**.
    *   *Note : En cas d'oubli de vos identifiants, contactez votre administrateur système.*

### Création de compte
Pour des raisons de sécurité, il n'y a pas d'inscription publique.
1.  **Administrateurs seulement** : Accédez à la section **"Utilisateurs"** dans le menu de navigation.
2.  Cliquez sur **"Ajouter un utilisateur"**.
3.  Remplissez le formulaire (Nom, prénom, téléphone, rôle, mot de passe).
4.  Le nouvel utilisateur pourra alors se connecter avec ses identifiants.

---

## 4. Utilisation : Étape par étape

### A. Configuration initiale (Admin)
Avant de commencer les emprunts :
1.  **Catégories** : Créez les thématiques (ex: Roman, Science, Histoire).
2.  **Livres** : Ajoutez vos ouvrages en précisant la quantité disponible.
3.  **Paramètres** : Définissez la durée maximale d'emprunt (ex: 14 jours) et la pénalité journalière de retard (ex: 100 FCFA).

### B. Enregistrement d'un lecteur
Tout emprunt nécessite un lecteur enregistré :
1.  Allez dans **"Lecteurs"** > **"Enregistrer un lecteur"**.
2.  Saisissez ses coordonnées complètes.

### C. Effectuer un emprunt
1.  Allez dans **"Nouveau Emprunt"** (ou cliquez sur le bouton "+" depuis la fiche d'un lecteur).
2.  Sélectionnez le **Lecteur** et le **Livre**.
3.  La date de retour prévue est calculée automatiquement selon les paramètres.
4.  Cliquez sur **"Enregistrer"**.
    *   *Système de contrôle : L'emprunt est bloqué si le livre n'est plus en stock ou si le lecteur a dépassé son quota.*

### D. Enregistrer un retour
1.  Dans la liste des **"Emprunts en cours"**, identifiez la ligne correspondante.
2.  Cliquez sur le bouton **"Retourner"** (icône de flèche).
3.  Vérifiez les éventuels jours de retard. La pénalité est calculée instantanément.
4.  Validez le retour. Le livre redevient disponible pour d'autres lecteurs.

---

## 5. Cas pratique : Exemple réel d’utilisation

**Contexte** : M. Jean Dupont souhaite emprunter le livre "L'Enfant Noir".

1.  **Vérification** : Le gestionnaire recherche "L'Enfant Noir" dans **"Livres"**. Il voit qu'il reste 2 exemplaires disponibles.
2.  **Action** : Le gestionnaire va dans **"Nouveau Emprunt"**.
    *   Il sélectionne "Jean Dupont".
    *   Il sélectionne "L'Enfant Noir".
    *   Le système indique que le livre doit être rendu dans 14 jours (ex: le 7 Avril).
3.  **Confirmation** : Jean repart avec le livre. Le stock passe de 2 à 1 disponible.
4.  **Scénario de retard** : Jean ramène le livre avec 3 jours de retard.
    *   Le gestionnaire clique sur **"Retourner"**.
    *   Le système affiche : "3 jours de retard. Pénalité : 300 FCFA".
    *   Après validation, le stock remonte à 2 disponibles.
