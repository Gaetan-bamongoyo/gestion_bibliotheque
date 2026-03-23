from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class Utilisateur(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Administrateur'),
        ('gestionnaire', 'Gestionnaire'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='gestionnaire')
    telephone = models.CharField(max_length=20, blank=True)

    def est_admin(self):
        return self.role == 'admin'

    def est_gestionnaire(self):
        return self.role == 'gestionnaire'

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"

    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'


class Categorie(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = 'Catégorie'
        verbose_name_plural = 'Catégories'
        ordering = ['nom']


class Livre(models.Model):
    titre = models.CharField(max_length=200)
    auteur = models.CharField(max_length=200)
    categorie = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True, blank=True, related_name='livres')
    isbn = models.CharField(max_length=20, blank=True)
    annee_publication = models.IntegerField(null=True, blank=True)
    editeur = models.CharField(max_length=150, blank=True)
    quantite_totale = models.PositiveIntegerField(default=1)
    quantite_disponible = models.PositiveIntegerField(default=1)
    description = models.TextField(blank=True)
    date_ajout = models.DateTimeField(auto_now_add=True)

    def est_disponible(self):
        return self.quantite_disponible > 0

    def __str__(self):
        return f"{self.titre} — {self.auteur}"

    class Meta:
        verbose_name = 'Livre'
        verbose_name_plural = 'Livres'
        ordering = ['titre']


class Lecteur(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    telephone = models.CharField(max_length=20, blank=True)
    adresse = models.TextField(blank=True)
    date_inscription = models.DateField(default=timezone.now)
    actif = models.BooleanField(default=True)

    def nom_complet(self):
        return f"{self.prenom} {self.nom}"

    def emprunts_en_cours(self):
        return self.emprunts.filter(statut__in=['en_cours', 'en_retard']).count()

    def __str__(self):
        return self.nom_complet()

    class Meta:
        verbose_name = 'Lecteur'
        verbose_name_plural = 'Lecteurs'
        ordering = ['nom', 'prenom']


class Emprunt(models.Model):
    STATUT_CHOICES = [
        ('en_cours', 'En cours'),
        ('retourne', 'Retourné'),
        ('en_retard', 'En retard'),
    ]
    lecteur = models.ForeignKey(Lecteur, on_delete=models.CASCADE, related_name='emprunts')
    livre = models.ForeignKey(Livre, on_delete=models.CASCADE, related_name='emprunts')
    date_emprunt = models.DateField(default=timezone.now)
    date_retour_prevue = models.DateField()
    date_retour_effective = models.DateField(null=True, blank=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_cours')
    notes = models.TextField(blank=True)
    penalite = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    enregistre_par = models.ForeignKey(
        Utilisateur, on_delete=models.SET_NULL, null=True, blank=True, related_name='emprunts_geres'
    )

    def jours_retard(self):
        if self.statut == 'retourne' and self.date_retour_effective:
            delta = self.date_retour_effective - self.date_retour_prevue
        else:
            from datetime import date
            delta = date.today() - self.date_retour_prevue
        return max(0, delta.days)

    def calculer_penalite(self, tarif_journalier=100):
        return self.jours_retard() * tarif_journalier

    def __str__(self):
        return f"Emprunt #{self.pk} — {self.lecteur} / {self.livre}"

    class Meta:
        verbose_name = 'Emprunt'
        verbose_name_plural = 'Emprunts'
        ordering = ['-date_emprunt']


class ParametreEmprunt(models.Model):
    nb_max_livres = models.PositiveIntegerField(default=3, help_text="Nombre maximum de livres par lecteur")
    duree_emprunt_jours = models.PositiveIntegerField(default=14, help_text="Durée d'emprunt en jours")
    penalite_par_jour = models.DecimalField(max_digits=8, decimal_places=2, default=100, help_text="Pénalité par jour de retard (FCFA)")
    mise_a_jour = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Paramètres d'emprunt (max {self.nb_max_livres} livres, {self.duree_emprunt_jours} jours)"

    class Meta:
        verbose_name = 'Paramètre d\'emprunt'
        verbose_name_plural = 'Paramètres d\'emprunt'
