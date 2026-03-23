from django.core.management.base import BaseCommand
from bibliotheque.models import Utilisateur, Categorie, Livre, Lecteur, Emprunt, ParametreEmprunt
from datetime import date, timedelta


class Command(BaseCommand):
    help = 'Initialise les données de démonstration pour la bibliothèque'

    def handle(self, *args, **options):
        self.stdout.write('Initialisation des données...')

        # Create admin user
        if not Utilisateur.objects.filter(username='admin').exists():
            admin = Utilisateur.objects.create_superuser(
                username='admin',
                email='admin@bibliotheque.cm',
                password='admin123',
                first_name='Super',
                last_name='Administrateur',
                role='admin'
            )
            self.stdout.write(self.style.SUCCESS('✓ Administrateur créé: admin / admin123'))
        else:
            self.stdout.write('→ Administrateur déjà existant')

        # Create gestionnaire
        if not Utilisateur.objects.filter(username='gestionnaire1').exists():
            Utilisateur.objects.create_user(
                username='gestionnaire1',
                email='gestionnaire@bibliotheque.cm',
                password='gest123',
                first_name='Marie',
                last_name='Nkolo',
                role='gestionnaire'
            )
            self.stdout.write(self.style.SUCCESS('✓ Gestionnaire créé: gestionnaire1 / gest123'))

        # Categories
        categories_data = [
            ('Informatique', 'Livres sur la programmation, les réseaux, l\'IA et l\'informatique générale'),
            ('Mathématiques', 'Algèbre, Analyse, Probabilités, Statistiques'),
            ('Physique', 'Mécanique, Thermodynamique, Électromagnétisme'),
            ('Littérature', 'Romans, Poésie, Théâtre africain et mondial'),
            ('Histoire', 'Histoire de l\'Afrique, Histoire universelle'),
            ('Économie', 'Microéconomie, Macroéconomie, Finance'),
            ('Droit', 'Droit civil, Droit des affaires, Droit international'),
            ('Sciences Sociales', 'Sociologie, Psychologie, Anthropologie'),
        ]
        categories = {}
        for nom, desc in categories_data:
            cat, created = Categorie.objects.get_or_create(nom=nom, defaults={'description': desc})
            categories[nom] = cat
            if created:
                self.stdout.write(f'✓ Catégorie: {nom}')

        # Books
        livres_data = [
            ('Introduction à Python', 'Guido van Rossum', 'Informatique', '978-2-01-234567-8', 2022, 'Eyrolles', 5),
            ('Algorithmes et structures de données', 'Thomas H. Cormen', 'Informatique', '978-0-26-204630-5', 2009, 'MIT Press', 3),
            ('Réseaux et Télécommunications', 'Andrew Tanenbaum', 'Informatique', '978-2-74-400922-3', 2020, 'Pearson', 4),
            ('Intelligence Artificielle', 'Stuart Russell', 'Informatique', '978-0-13-604259-4', 2021, 'Pearson', 2),
            ('Analyse Mathématique T1', 'Walter Rudin', 'Mathématiques', '978-2-10-003234-1', 2019, 'Dunod', 4),
            ('Algèbre Linéaire', 'Gilbert Strang', 'Mathématiques', '978-0-98-026005-9', 2016, 'Wellesley', 3),
            ('Probabilités et Statistiques', 'Paul Lévy', 'Mathématiques', '978-2-10-055123-7', 2018, 'Dunod', 2),
            ('Mécanique Quantique', 'Cohen-Tannoudji', 'Physique', '978-2-10-003441-3', 2018, 'EDP Sciences', 2),
            ('Les Soleils des Indépendances', 'Ahmadou Kourouma', 'Littérature', '978-2-07-036822-6', 1970, 'Seuil', 3),
            ('Sous l\'orage', 'Seydou Badian', 'Littérature', '978-2-70-803012-9', 1957, 'Présence Africaine', 4),
            ('Histoire Générale de l\'Afrique', 'UNESCO', 'Histoire', '978-9-23-102059-4', 1999, 'UNESCO', 3),
            ('Droit des obligations', 'François Terré', 'Droit', '978-2-24-727698-6', 2019, 'Dalloz', 2),
            ('Principes d\'Économie', 'N. Gregory Mankiw', 'Économie', '978-2-80-411328-1', 2020, 'De Boeck', 4),
            ('Sociologie', 'Anthony Giddens', 'Sciences Sociales', '978-2-70-118273-2', 2014, 'Eyrolles', 3),
        ]
        for titre, auteur, cat_nom, isbn, annee, editeur, qte in livres_data:
            livre, created = Livre.objects.get_or_create(
                titre=titre,
                defaults={
                    'auteur': auteur,
                    'categorie': categories.get(cat_nom),
                    'isbn': isbn,
                    'annee_publication': annee,
                    'editeur': editeur,
                    'quantite_totale': qte,
                    'quantite_disponible': qte
                }
            )
            if created:
                self.stdout.write(f'✓ Livre: {titre}')

        # Readers
        lecteurs_data = [
            ('Mballa', 'Emmanuel', 'emmanuel.mballa@univ.cm', '6 77 11 22 33', 'Yaoundé, Mfandena'),
            ('Ndzana', 'Célestine', 'celestine.ndzana@univ.cm', '6 99 44 55 66', 'Yaoundé, Bastos'),
            ('Fouda', 'Patrick', 'patrick.fouda@univ.cm', '6 55 77 88 99', 'Douala, Bonamoussadi'),
            ('Biyong', 'Nadège', 'nadege.biyong@univ.cm', '6 72 33 44 55', 'Yaoundé, Melen'),
            ('Ekwalla', 'Serge', 'serge.ekwalla@univ.cm', '6 98 22 11 66', 'Douala, Akwa'),
            ('Ondoua', 'Marie-Claire', 'marieclaire.ondoua@univ.cm', '6 55 88 77 44', 'Yaoundé, Ngousso'),
            ('Nkodo', 'Jean-Pierre', 'jeanpierre.nkodo@univ.cm', '6 71 99 33 00', 'Bafoussam, Centre'),
            ('Atanga', 'Lara', 'lara.atanga@univ.cm', '6 90 55 44 88', 'Yaoundé, Elig-Essono'),
        ]
        lecteurs = []
        for nom, prenom, email, tel, adresse in lecteurs_data:
            lecteur, created = Lecteur.objects.get_or_create(
                nom=nom, prenom=prenom,
                defaults={'email': email, 'telephone': tel, 'adresse': adresse}
            )
            lecteurs.append(lecteur)
            if created:
                self.stdout.write(f'✓ Lecteur: {prenom} {nom}')

        # Default params
        params, created = ParametreEmprunt.objects.get_or_create(pk=1, defaults={
            'nb_max_livres': 3,
            'duree_emprunt_jours': 14,
            'penalite_par_jour': 100
        })
        if created:
            self.stdout.write('✓ Paramètres d\'emprunt créés')

        # Sample loans
        if Emprunt.objects.count() == 0 and Livre.objects.count() > 0 and len(lecteurs) > 0:
            admin_user = Utilisateur.objects.filter(role='admin').first()
            livres_list = list(Livre.objects.all()[:6])
            today = date.today()

            emprunts_sample = [
                (lecteurs[0], livres_list[0], today - timedelta(days=5), today + timedelta(days=9), None, 'en_cours'),
                (lecteurs[1], livres_list[1], today - timedelta(days=20), today - timedelta(days=6), today - timedelta(days=2), 'retourne'),
                (lecteurs[2], livres_list[2], today - timedelta(days=18), today - timedelta(days=4), None, 'en_retard'),
                (lecteurs[3], livres_list[3], today - timedelta(days=3), today + timedelta(days=11), None, 'en_cours'),
                (lecteurs[4], livres_list[4], today - timedelta(days=15), today - timedelta(days=1), None, 'en_retard'),
            ]

            for lecteur, livre, d_emp, d_prev, d_eff, statut in emprunts_sample:
                if livre.quantite_disponible > 0 or statut == 'retourne':
                    if statut != 'retourne':
                        livre.quantite_disponible = max(0, livre.quantite_disponible - 1)
                        livre.save()
                    Emprunt.objects.create(
                        lecteur=lecteur,
                        livre=livre,
                        date_emprunt=d_emp,
                        date_retour_prevue=d_prev,
                        date_retour_effective=d_eff,
                        statut=statut,
                        enregistre_par=admin_user
                    )
            self.stdout.write('✓ Emprunts de démonstration créés')

        self.stdout.write(self.style.SUCCESS('\n✅ Initialisation terminée !'))
        self.stdout.write(self.style.SUCCESS('   → Connectez-vous sur http://127.0.0.1:8000/'))
        self.stdout.write(self.style.SUCCESS('   → Admin:        admin / admin123'))
        self.stdout.write(self.style.SUCCESS('   → Gestionnaire: gestionnaire1 / gest123'))
