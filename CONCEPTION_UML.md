# Conception UML — Gestion de Bibliothèque ISP/Isiro

Ce document présente la modélisation UML du système de gestion de bibliothèque numérique.

## 1. Diagramme de Cas d'Utilisation (Use Case Diagram)

Le système distingue deux types d'acteurs : l'**Administrateur** et le **Gestionnaire**.

```mermaid
useCaseDiagram
    actor "Administrateur" as Admin
    actor "Gestionnaire" as Gest

    package "Système de Gestion de Bibliothèque" {
        usecase "S'authentifier" as UC1
        usecase "Gérer les Livres (CRUD)" as UC2
        usecase "Gérer les Catégories" as UC3
        usecase "Gérer les Lecteurs" as UC4
        usecase "Enregistrer un Emprunt" as UC5
        usecase "Enregistrer un Retour" as UC6
        usecase "Générer Rapport d'Emprunts" as UC7
        usecase "Consulter les Statistiques" as UC8
        usecase "Gérer les Utilisateurs" as UC9
        usecase "Configurer les Paramètres" as UC10
    }

    Admin --> UC1
    Admin --> UC2
    Admin --> UC3
    Admin --> UC9
    Admin --> UC10
    
    Gest --> UC1
    Gest --> UC4
    Gest --> UC5
    Gest --> UC6
    Gest --> UC7
    Gest --> UC8
    
    %% Héritage des droits
    Admin --|> Gest
```

---

## 2. Diagramme de Classes (Class Diagram)

Ce diagramme représente la structure des données et les relations entre les différentes entités du projet Django.

```mermaid
classDiagram
    class Utilisateur {
        +String username
        +String email
        +String role (admin/gestionnaire)
        +String telephone
        +est_admin() bool
        +est_gestionnaire() bool
    }

    class Categorie {
        +String nom
        +String description
        +DateTime date_creation
    }

    class Livre {
        +String titre
        +String auteur
        +String isbn
        +Integer annee_publication
        +Integer quantite_totale
        +Integer quantite_disponible
        +est_disponible() bool
    }

    class Lecteur {
        +String nom
        +String prenom
        +String email
        +String telephone
        +Date date_inscription
        +Boolean actif
        +nom_complet() String
        +emprunts_en_cours() Integer
    }

    class Emprunt {
        +Date date_emprunt
        +Date date_retour_prevue
        +Date date_retour_effective
        +String statut (en_cours/retourne/en_retard)
        +Decimal penalite
        +jours_retard() Integer
        +calculer_penalite() Decimal
    }

    class ParametreEmprunt {
        +Integer nb_max_livres
        +Integer duree_emprunt_jours
        +Decimal penalite_par_jour
    }

    Livre "*" --> "0..1" Categorie : appartient à
    Emprunt "*" --> "1" Lecteur : effectué par
    Emprunt "*" --> "1" Livre : concerne
    Emprunt "*" --> "0..1" Utilisateur : enregistré par
    Lecteur "1" -- "*" Emprunt : possède
```

---

## 3. Description des Relations

- **Livre & Catégorie** : Un livre peut appartenir à une seule catégorie, tandis qu'une catégorie peut regrouper plusieurs livres.
- **Emprunt & Lecteur** : Un lecteur peut effectuer plusieurs emprunts au fil du temps.
- **Emprunt & Livre** : Chaque enregistrement d'emprunt lie un lecteur spécifique à un livre spécifique.
- **Utilisateur & Emprunt** : Le système garde une trace du gestionnaire ayant validé chaque transaction (traçabilité).

---

## 4. Diagramme de Séquence (Sequence Diagram)

Ce diagramme illustre le processus métier typique d'un **nouvel emprunt**.

```mermaid
sequenceDiagram
    autonumber
    actor L as Lecteur
    actor G as Gestionnaire
    participant S as Système (Django/Base de données)

    L->>G: Présente sa demande d'emprunt
    G->>S: Saisit l'emprunteur et le livre
    S->>S: Vérifie disponibilité du livre
    S->>S: Vérifie limite d'emprunts du lecteur
    alt Possible
        S-->>G: Confirmation de succès
        S->>S: Décrémente quantité disponible
        G-->>L: Remet le livre
    else Erreur (Livre non disp. ou Max atteint)
        S-->>G: Alerte d'erreur
        G-->>L: Explique le refus
    end
```

---

## 5. Diagramme d'États (State Diagram)

Ce diagramme montre le cycle de vie d'un **Emprunt** dans le système.

```mermaid
stateDiagram-v2
    [*] --> EnCours : Création de l'emprunt
    
    EnCours --> Retourne : Retour du livre (avant échéance)
    EnCours --> EnRetard : Date de retour prévue dépassée
    
    EnRetard --> Retourne : Retour du livre (+ pénalité calculée)
    
    Retourne --> [*] : Transaction clôturée
```

> [!TIP]
> Ce document sert de base pour toute évolution future du schéma de base de données ou pour la formation de nouveaux développeurs sur le projet.
