from django.urls import path
from . import views

app_name = 'bibliotheque'

urlpatterns = [
    # Auth
    path('', views.connexion, name='connexion'),
    path('connexion/', views.connexion, name='connexion'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),

    # Dashboard
    path('tableau-de-bord/', views.tableau_bord, name='tableau_bord'),

    # Livres
    path('livres/', views.liste_livres, name='liste_livres'),
    path('livres/ajouter/', views.ajouter_livre, name='ajouter_livre'),
    path('livres/<int:pk>/modifier/', views.modifier_livre, name='modifier_livre'),
    path('livres/<int:pk>/supprimer/', views.supprimer_livre, name='supprimer_livre'),

    # Catégories
    path('categories/', views.liste_categories, name='liste_categories'),
    path('categories/ajouter/', views.ajouter_categorie, name='ajouter_categorie'),
    path('categories/<int:pk>/modifier/', views.modifier_categorie, name='modifier_categorie'),
    path('categories/<int:pk>/supprimer/', views.supprimer_categorie, name='supprimer_categorie'),

    # Lecteurs
    path('lecteurs/', views.liste_lecteurs, name='liste_lecteurs'),
    path('lecteurs/ajouter/', views.ajouter_lecteur, name='ajouter_lecteur'),
    path('lecteurs/<int:pk>/', views.detail_lecteur, name='detail_lecteur'),
    path('lecteurs/<int:pk>/modifier/', views.modifier_lecteur, name='modifier_lecteur'),
    path('lecteurs/<int:pk>/supprimer/', views.supprimer_lecteur, name='supprimer_lecteur'),

    # Emprunts
    path('emprunts/', views.liste_emprunts, name='liste_emprunts'),
    path('emprunts/nouveau/', views.nouvel_emprunt, name='nouvel_emprunt'),
    path('emprunts/<int:pk>/retour/', views.retour_livre, name='retour_livre'),

    # Historique
    path('historique/', views.historique, name='historique'),

    # Statistiques
    path('statistiques/', views.statistiques, name='statistiques'),

    # Gestion des utilisateurs (admin)
    path('utilisateurs/', views.liste_gestionnaires, name='liste_gestionnaires'),
    path('utilisateurs/ajouter/', views.ajouter_gestionnaire, name='ajouter_gestionnaire'),
    path('utilisateurs/<int:pk>/modifier/', views.modifier_gestionnaire, name='modifier_gestionnaire'),
    path('utilisateurs/<int:pk>/supprimer/', views.supprimer_gestionnaire, name='supprimer_gestionnaire'),

    # Paramètres (admin)
    path('parametres/', views.parametres, name='parametres'),
]
