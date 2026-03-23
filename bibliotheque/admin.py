from django.contrib import admin
from .models import Utilisateur, Categorie, Livre, Lecteur, Emprunt, ParametreEmprunt


@admin.register(Utilisateur)
class UtilisateurAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email', 'role', 'is_active']
    list_filter = ['role', 'is_active']
    search_fields = ['username', 'first_name', 'last_name', 'email']


@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ['nom', 'description', 'date_creation']
    search_fields = ['nom']


@admin.register(Livre)
class LivreAdmin(admin.ModelAdmin):
    list_display = ['titre', 'auteur', 'categorie', 'quantite_totale', 'quantite_disponible', 'date_ajout']
    list_filter = ['categorie']
    search_fields = ['titre', 'auteur', 'isbn']


@admin.register(Lecteur)
class LecteurAdmin(admin.ModelAdmin):
    list_display = ['nom', 'prenom', 'email', 'telephone', 'date_inscription', 'actif']
    list_filter = ['actif']
    search_fields = ['nom', 'prenom', 'email', 'telephone']


@admin.register(Emprunt)
class EmpruntAdmin(admin.ModelAdmin):
    list_display = ['lecteur', 'livre', 'date_emprunt', 'date_retour_prevue', 'date_retour_effective', 'statut']
    list_filter = ['statut']
    search_fields = ['lecteur__nom', 'livre__titre']


@admin.register(ParametreEmprunt)
class ParametreEmpruntAdmin(admin.ModelAdmin):
    list_display = ['nb_max_livres', 'duree_emprunt_jours', 'penalite_par_jour', 'mise_a_jour']
