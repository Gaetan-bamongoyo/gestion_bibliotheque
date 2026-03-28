from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q, Count
from django.utils import timezone
from datetime import date, timedelta
from decimal import Decimal

from .models import Utilisateur, Categorie, Livre, Lecteur, Emprunt, ParametreEmprunt
from .forms import (
    ConnexionForm, GestionnaireForm, CategorieForm,
    LivreForm, LecteurForm, EmpruntForm, RetourForm, ParametreForm
)
from .decorators import admin_required, gestionnaire_ou_admin_required


# ─── Auth ──────────────────────────────────────────────────────────────────────

def connexion(request):
    if request.user.is_authenticated:
        return redirect('bibliotheque:tableau_bord')
    form = ConnexionForm(request, data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Bienvenue, {user.get_full_name() or user.username} !")
            return redirect('bibliotheque:tableau_bord')
        else:
            messages.error(request, "Identifiant ou mot de passe incorrect.")
    return render(request, 'bibliotheque/login.html', {'form': form})


def deconnexion(request):
    logout(request)
    messages.success(request, "Vous avez été déconnecté.")
    return redirect('bibliotheque:connexion')


# ─── Mise à jour automatique des statuts ───────────────────────────────────────

def mettre_a_jour_retards():
    """Mark overdue loans automatically."""
    today = date.today()
    Emprunt.objects.filter(
        statut='en_cours',
        date_retour_prevue__lt=today
    ).update(statut='en_retard')


# ─── Dashboard ─────────────────────────────────────────────────────────────────

@gestionnaire_ou_admin_required
def tableau_bord(request):
    mettre_a_jour_retards()
    total_livres = Livre.objects.count()
    livres_disponibles = Livre.objects.filter(quantite_disponible__gt=0).count()
    livres_empruntes = Emprunt.objects.filter(statut__in=['en_cours', 'en_retard']).count()
    total_lecteurs = Lecteur.objects.filter(actif=True).count()
    total_retards = Emprunt.objects.filter(statut='en_retard').count()
    emprunts_recents = Emprunt.objects.select_related('lecteur', 'livre').order_by('-date_emprunt')[:5]
    retards = Emprunt.objects.select_related('lecteur', 'livre').filter(statut='en_retard').order_by('date_retour_prevue')[:5]

    context = {
        'total_livres': total_livres,
        'livres_disponibles': livres_disponibles,
        'livres_empruntes': livres_empruntes,
        'total_lecteurs': total_lecteurs,
        'total_retards': total_retards,
        'emprunts_recents': emprunts_recents,
        'retards': retards,
    }
    return render(request, 'bibliotheque/dashboard.html', context)


# ─── Livres ────────────────────────────────────────────────────────────────────

@gestionnaire_ou_admin_required
def liste_livres(request):
    q = request.GET.get('q', '')
    categorie_id = request.GET.get('categorie', '')
    livres = Livre.objects.select_related('categorie').all()
    if q:
        livres = livres.filter(Q(titre__icontains=q) | Q(auteur__icontains=q) | Q(isbn__icontains=q))
    if categorie_id:
        livres = livres.filter(categorie_id=categorie_id)
    categories = Categorie.objects.all()
    return render(request, 'bibliotheque/livres/liste.html', {
        'livres': livres, 'categories': categories, 'q': q, 'categorie_id': categorie_id
    })


@admin_required
def ajouter_livre(request):
    form = LivreForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Livre ajouté avec succès.")
        return redirect('bibliotheque:liste_livres')
    return render(request, 'bibliotheque/livres/form.html', {'form': form, 'titre': 'Ajouter un livre'})


@admin_required
def modifier_livre(request, pk):
    livre = get_object_or_404(Livre, pk=pk)
    form = LivreForm(request.POST or None, instance=livre)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Livre modifié avec succès.")
        return redirect('bibliotheque:liste_livres')
    return render(request, 'bibliotheque/livres/form.html', {'form': form, 'titre': 'Modifier le livre', 'livre': livre})


@admin_required
def supprimer_livre(request, pk):
    livre = get_object_or_404(Livre, pk=pk)
    if request.method == 'POST':
        livre.delete()
        messages.success(request, "Livre supprimé.")
        return redirect('bibliotheque:liste_livres')
    return render(request, 'bibliotheque/confirm_delete.html', {'objet': livre, 'type': 'livre'})


# ─── Catégories ────────────────────────────────────────────────────────────────

@admin_required
def liste_categories(request):
    categories = Categorie.objects.annotate(nb_livres=Count('livres')).order_by('nom')
    return render(request, 'bibliotheque/categories/liste.html', {'categories': categories})


@admin_required
def ajouter_categorie(request):
    form = CategorieForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Catégorie ajoutée.")
        return redirect('bibliotheque:liste_categories')
    return render(request, 'bibliotheque/categories/form.html', {'form': form, 'titre': 'Ajouter une catégorie'})


@admin_required
def modifier_categorie(request, pk):
    cat = get_object_or_404(Categorie, pk=pk)
    form = CategorieForm(request.POST or None, instance=cat)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Catégorie modifiée.")
        return redirect('bibliotheque:liste_categories')
    return render(request, 'bibliotheque/categories/form.html', {'form': form, 'titre': 'Modifier la catégorie', 'categorie': cat})


@admin_required
def supprimer_categorie(request, pk):
    cat = get_object_or_404(Categorie, pk=pk)
    if request.method == 'POST':
        cat.delete()
        messages.success(request, "Catégorie supprimée.")
        return redirect('bibliotheque:liste_categories')
    return render(request, 'bibliotheque/confirm_delete.html', {'objet': cat, 'type': 'catégorie'})


# ─── Lecteurs ──────────────────────────────────────────────────────────────────

@gestionnaire_ou_admin_required
def liste_lecteurs(request):
    q = request.GET.get('q', '')
    lecteurs = Lecteur.objects.all()
    if q:
        lecteurs = lecteurs.filter(Q(nom__icontains=q) | Q(prenom__icontains=q) | Q(email__icontains=q) | Q(telephone__icontains=q))
    return render(request, 'bibliotheque/lecteurs/liste.html', {'lecteurs': lecteurs, 'q': q})


@gestionnaire_ou_admin_required
def ajouter_lecteur(request):
    form = LecteurForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Lecteur enregistré avec succès.")
        return redirect('bibliotheque:liste_lecteurs')
    return render(request, 'bibliotheque/lecteurs/form.html', {'form': form, 'titre': 'Enregistrer un lecteur'})


@gestionnaire_ou_admin_required
def modifier_lecteur(request, pk):
    lecteur = get_object_or_404(Lecteur, pk=pk)
    form = LecteurForm(request.POST or None, instance=lecteur)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Lecteur modifié.")
        return redirect('bibliotheque:liste_lecteurs')
    return render(request, 'bibliotheque/lecteurs/form.html', {'form': form, 'titre': 'Modifier le lecteur', 'lecteur': lecteur})


@admin_required
def supprimer_lecteur(request, pk):
    lecteur = get_object_or_404(Lecteur, pk=pk)
    if request.method == 'POST':
        lecteur.delete()
        messages.success(request, "Lecteur supprimé.")
        return redirect('bibliotheque:liste_lecteurs')
    return render(request, 'bibliotheque/confirm_delete.html', {'objet': lecteur, 'type': 'lecteur'})


@gestionnaire_ou_admin_required
def detail_lecteur(request, pk):
    lecteur = get_object_or_404(Lecteur, pk=pk)
    emprunts = lecteur.emprunts.select_related('livre').order_by('-date_emprunt')
    return render(request, 'bibliotheque/lecteurs/detail.html', {'lecteur': lecteur, 'emprunts': emprunts})


# ─── Emprunts ──────────────────────────────────────────────────────────────────

@gestionnaire_ou_admin_required
def liste_emprunts(request):
    mettre_a_jour_retards()
    statut = request.GET.get('statut', '')
    q = request.GET.get('q', '')
    lettre = request.GET.get('lettre', '')
    
    emprunts = Emprunt.objects.select_related('lecteur', 'livre').all()
    if statut:
        emprunts = emprunts.filter(statut=statut)
    if q:
        emprunts = emprunts.filter(
            Q(lecteur__nom__icontains=q) | Q(lecteur__prenom__icontains=q) | Q(livre__titre__icontains=q)
        )
    if lettre:
        emprunts = emprunts.filter(lecteur__nom__istartswith=lettre)

    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    return render(request, 'bibliotheque/emprunts/liste.html', {
        'emprunts': emprunts, 
        'statut': statut, 
        'q': q,
        'alphabet': alphabet,
        'lettre_active': lettre
    })


@gestionnaire_ou_admin_required
def nouvel_emprunt(request):
    # Pre-select lecteur if passed via GET
    initial = {}
    lecteur_id = request.GET.get('lecteur')
    if lecteur_id:
        initial['lecteur'] = lecteur_id

    form = EmpruntForm(request.POST or None, initial=initial)
    if request.method == 'POST' and form.is_valid():
        emprunt = form.save(commit=False)
        lecteur = emprunt.lecteur

        # Check max loans
        try:
            params = ParametreEmprunt.objects.first()
            max_livres = params.nb_max_livres if params else 3
        except Exception:
            max_livres = 3

        emprunts_actifs = lecteur.emprunts_en_cours()
        if emprunts_actifs >= max_livres:
            messages.error(request, f"Ce lecteur a déjà {emprunts_actifs} emprunt(s) en cours (maximum : {max_livres}).")
            return render(request, 'bibliotheque/emprunts/form.html', {'form': form, 'titre': 'Nouvel emprunt'})

        livre = emprunt.livre
        if livre.quantite_disponible < 1:
            messages.error(request, "Ce livre n'est plus disponible.")
            return render(request, 'bibliotheque/emprunts/form.html', {'form': form, 'titre': 'Nouvel emprunt'})

        emprunt.statut = 'en_cours'
        emprunt.enregistre_par = request.user
        emprunt.save()

        # Decrease available count
        livre.quantite_disponible -= 1
        livre.save()

        messages.success(request, f"Emprunt enregistré pour {lecteur.nom_complet()}.")
        return redirect('bibliotheque:liste_emprunts')

    return render(request, 'bibliotheque/emprunts/form.html', {'form': form, 'titre': 'Nouvel emprunt'})


@gestionnaire_ou_admin_required
def retour_livre(request, pk):
    emprunt = get_object_or_404(Emprunt, pk=pk)
    if emprunt.statut == 'retourne':
        messages.info(request, "Ce livre a déjà été retourné.")
        return redirect('bibliotheque:liste_emprunts')

    form = RetourForm(request.POST or None, instance=emprunt)
    if request.method == 'POST' and form.is_valid():
        emprunt = form.save(commit=False)
        emprunt.statut = 'retourne'

        # Calculate penalty
        try:
            params = ParametreEmprunt.objects.first()
            tarif = float(params.penalite_par_jour) if params else 100
        except Exception:
            tarif = 100

        jours = emprunt.jours_retard()
        emprunt.penalite = Decimal(str(jours * tarif))
        emprunt.save()

        # Restore available count
        livre = emprunt.livre
        livre.quantite_disponible += 1
        livre.save()

        if emprunt.penalite > 0:
            messages.warning(request, f"Retour enregistré avec {jours} jour(s) de retard. Pénalité : {emprunt.penalite:.0f} FCFA.")
        else:
            messages.success(request, "Retour enregistré avec succès.")
        return redirect('bibliotheque:liste_emprunts')

    return render(request, 'bibliotheque/emprunts/retour.html', {'form': form, 'emprunt': emprunt})


# ─── Historique ────────────────────────────────────────────────────────────────

@gestionnaire_ou_admin_required
def historique(request):
    emprunts = Emprunt.objects.select_related('lecteur', 'livre', 'enregistre_par').order_by('-date_emprunt')
    q = request.GET.get('q', '')
    if q:
        emprunts = emprunts.filter(
            Q(lecteur__nom__icontains=q) | Q(lecteur__prenom__icontains=q) | Q(livre__titre__icontains=q)
        )
    return render(request, 'bibliotheque/historique.html', {'emprunts': emprunts, 'q': q})


# ─── Statistiques ──────────────────────────────────────────────────────────────

@gestionnaire_ou_admin_required
def statistiques(request):
    mettre_a_jour_retards()
    total_livres = Livre.objects.count()
    livres_disponibles = Livre.objects.filter(quantite_disponible__gt=0).count()
    total_lecteurs = Lecteur.objects.count()
    total_emprunts = Emprunt.objects.count()
    emprunts_en_cours = Emprunt.objects.filter(statut__in=['en_cours', 'en_retard']).count()
    total_retards = Emprunt.objects.filter(statut='en_retard').count()
    emprunts_retournes = Emprunt.objects.filter(statut='retourne').count()

    # Books by category
    cat_data = Categorie.objects.annotate(nb=Count('livres')).order_by('-nb')
    cat_labels = [c.nom for c in cat_data]
    cat_values = [c.nb for c in cat_data]

    # Loans per month (last 6 months)
    from django.db.models.functions import TruncMonth
    six_months_ago = date.today() - timedelta(days=180)
    monthly = (
        Emprunt.objects.filter(date_emprunt__gte=six_months_ago)
        .annotate(mois=TruncMonth('date_emprunt'))
        .values('mois')
        .annotate(nb=Count('id'))
        .order_by('mois')
    )
    monthly_labels = [e['mois'].strftime('%b %Y') if e['mois'] else '' for e in monthly]
    monthly_values = [e['nb'] for e in monthly]

    # Top lecteurs
    top_lecteurs = (
        Lecteur.objects.annotate(nb_emprunts=Count('emprunts'))
        .order_by('-nb_emprunts')[:5]
    )

    # Top livres
    top_livres = (
        Livre.objects.annotate(nb_emprunts=Count('emprunts'))
        .order_by('-nb_emprunts')[:5]
    )

    context = {
        'total_livres': total_livres,
        'livres_disponibles': livres_disponibles,
        'total_lecteurs': total_lecteurs,
        'total_emprunts': total_emprunts,
        'emprunts_en_cours': emprunts_en_cours,
        'total_retards': total_retards,
        'emprunts_retournes': emprunts_retournes,
        'cat_labels': cat_labels,
        'cat_values': cat_values,
        'monthly_labels': monthly_labels,
        'monthly_values': monthly_values,
        'top_lecteurs': top_lecteurs,
        'top_livres': top_livres,
    }
    return render(request, 'bibliotheque/statistiques.html', context)


# ─── Gestionnaires (admin only) ────────────────────────────────────────────────

@admin_required
def liste_gestionnaires(request):
    utilisateurs = Utilisateur.objects.all().order_by('date_joined')
    return render(request, 'bibliotheque/gestionnaires/liste.html', {'utilisateurs': utilisateurs})


@admin_required
def ajouter_gestionnaire(request):
    form = GestionnaireForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Utilisateur créé avec succès.")
        return redirect('bibliotheque:liste_gestionnaires')
    return render(request, 'bibliotheque/gestionnaires/form.html', {'form': form, 'titre': 'Ajouter un utilisateur'})


@admin_required
def modifier_gestionnaire(request, pk):
    utilisateur = get_object_or_404(Utilisateur, pk=pk)
    form = GestionnaireForm(request.POST or None, instance=utilisateur)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Utilisateur modifié.")
        return redirect('bibliotheque:liste_gestionnaires')
    return render(request, 'bibliotheque/gestionnaires/form.html', {'form': form, 'titre': 'Modifier l\'utilisateur', 'utilisateur': utilisateur})


@admin_required
def supprimer_gestionnaire(request, pk):
    utilisateur = get_object_or_404(Utilisateur, pk=pk)
    if utilisateur == request.user:
        messages.error(request, "Vous ne pouvez pas supprimer votre propre compte.")
        return redirect('bibliotheque:liste_gestionnaires')
    if request.method == 'POST':
        utilisateur.delete()
        messages.success(request, "Utilisateur supprimé.")
        return redirect('bibliotheque:liste_gestionnaires')
    return render(request, 'bibliotheque/confirm_delete.html', {'objet': utilisateur, 'type': 'utilisateur'})


# ─── Paramètres (admin only) ───────────────────────────────────────────────────

@admin_required
def parametres(request):
    params, _ = ParametreEmprunt.objects.get_or_create(pk=1)
    form = ParametreForm(request.POST or None, instance=params)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Paramètres enregistrés.")
        return redirect('bibliotheque:parametres')
    return render(request, 'bibliotheque/parametres.html', {'form': form, 'params': params})


# ─── Rapports ──────────────────────────────────────────────────────────────────

@gestionnaire_ou_admin_required
def rapport_emprunts(request):
    date_str = request.GET.get('date', timezone.now().date().isoformat())
    lettre = request.GET.get('lettre', '')
    
    try:
        selection_date = date.fromisoformat(date_str)
    except (ValueError, TypeError):
        selection_date = timezone.now().date()

    emprunts = Emprunt.objects.filter(date_emprunt=selection_date).select_related('lecteur', 'livre', 'enregistre_par')
    
    if lettre:
        emprunts = emprunts.filter(lecteur__nom__istartswith=lettre)

    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    return render(request, 'bibliotheque/emprunts/date_report.html', {
        'emprunts': emprunts,
        'selection_date': selection_date,
        'today': timezone.now().date(),
        'alphabet': alphabet,
        'lettre_active': lettre
    })
