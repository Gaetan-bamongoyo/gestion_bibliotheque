from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Utilisateur, Categorie, Livre, Lecteur, Emprunt, ParametreEmprunt
from datetime import date, timedelta


class ConnexionForm(AuthenticationForm):
    username = forms.CharField(
        label="Nom d'utilisateur",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Nom d'utilisateur", 'autofocus': True})
    )
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mot de passe'})
    )


class GestionnaireForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Mot de passe',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mot de passe'}),
        required=False
    )
    password2 = forms.CharField(
        label='Confirmer le mot de passe',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmer le mot de passe'}),
        required=False
    )

    class Meta:
        model = Utilisateur
        fields = ['first_name', 'last_name', 'username', 'email', 'telephone', 'role', 'is_active']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Nom d'utilisateur"}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Téléphone'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password1')
        p2 = cleaned_data.get('password2')
        if p1 or p2:
            if p1 != p2:
                raise forms.ValidationError("Les mots de passe ne correspondent pas.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        p1 = self.cleaned_data.get('password1')
        if p1:
            user.set_password(p1)
        elif not user.pk:
            user.set_password('gestionnaire123')
        if commit:
            user.save()
        return user


class CategorieForm(forms.ModelForm):
    class Meta:
        model = Categorie
        fields = ['nom', 'description']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de la catégorie'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Description (optionnelle)'}),
        }


class LivreForm(forms.ModelForm):
    class Meta:
        model = Livre
        fields = ['titre', 'auteur', 'categorie', 'isbn', 'annee_publication', 'editeur', 'quantite_totale', 'quantite_disponible', 'description']
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre du livre'}),
            'auteur': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Auteur'}),
            'categorie': forms.Select(attrs={'class': 'form-select'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ISBN'}),
            'annee_publication': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Année'}),
            'editeur': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Éditeur'}),
            'quantite_totale': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'quantite_disponible': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Description'}),
        }


class LecteurForm(forms.ModelForm):
    class Meta:
        model = Lecteur
        fields = ['nom', 'prenom', 'email', 'telephone', 'adresse', 'date_inscription', 'actif']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Téléphone'}),
            'adresse': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Adresse'}),
            'date_inscription': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'actif': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class EmpruntForm(forms.ModelForm):
    class Meta:
        model = Emprunt
        fields = ['lecteur', 'livre', 'date_emprunt', 'date_retour_prevue', 'notes']
        widgets = {
            'lecteur': forms.Select(attrs={'class': 'form-select'}),
            'livre': forms.Select(attrs={'class': 'form-select'}),
            'date_emprunt': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_retour_prevue': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Notes (optionnel)'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show available books
        self.fields['livre'].queryset = Livre.objects.filter(quantite_disponible__gt=0)
        self.fields['lecteur'].queryset = Lecteur.objects.filter(actif=True)
        # Default dates
        if not self.instance.pk:
            today = date.today()
            self.fields['date_emprunt'].initial = today
            try:
                params = ParametreEmprunt.objects.first()
                duree = params.duree_emprunt_jours if params else 14
            except Exception:
                duree = 14
            self.fields['date_retour_prevue'].initial = today + timedelta(days=duree)


class RetourForm(forms.ModelForm):
    class Meta:
        model = Emprunt
        fields = ['date_retour_effective', 'notes']
        widgets = {
            'date_retour_effective': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Notes de retour'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date_retour_effective'].initial = date.today()


class ParametreForm(forms.ModelForm):
    class Meta:
        model = ParametreEmprunt
        fields = ['nb_max_livres', 'duree_emprunt_jours', 'penalite_par_jour']
        widgets = {
            'nb_max_livres': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'duree_emprunt_jours': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'penalite_par_jour': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': '0.01'}),
        }
