# 🔐 Système de Gestion des Comptes - Documentation Complète

## 📋 Vue d'ensemble

Un système complet de gestion d'utilisateurs avec trois types de rôles :
- **Étudiant** - Accès au catalogue et gestion des emprunts
- **Enseignant** - Accès étendu avec recommandations
- **Administrateur** - Accès complet à l'administration

## 🏗️ Architecture du Système

### Applications créées

#### 1. **Accounts** - Gestion des utilisateurs
```
Accounts/
├── managers.py          # Gestionnaire d'utilisateurs personnalisé
├── models.py            # Modèle User personnalisé
├── forms.py             # Formulaires d'inscription et connexion
├── views.py             # Vues d'authentification et tableaux de bord
├── urls.py              # Routes de l'application
├── admin.py             # Configuration de l'interface admin
└── templates/Accounts/  # Templates HTML
    ├── register.html
    ├── login.html
    ├── student_dashboard.html
    ├── teacher_dashboard.html
    └── admin_dashboard.html
```

#### 2. **profiles** - Profils utilisateurs
```
profiles/
├── models.py            # Modèles de profil (Student, Teacher, Admin)
├── signals.py           # Création automatique des profils
├── apps.py              # Configuration avec signaux
└── admin.py             # Administration des profils
```

## 🔧 Composants Principaux

### 1. Modèle User Personnalisé

**Fichier:** [Accounts/models.py](Accounts/models.py)

- Utilise l'email comme identifiant unique (au lieu du username)
- Champs de rôle : STUDENT, TEACHER, ADMIN
- Champs supplémentaires : phone, created_at, updated_at

```python
class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=STUDENT)
    phone = models.CharField(max_length=20, blank=True, null=True)
    
    USERNAME_FIELD = "email"
    objects = CustomUserManager()
```

### 2. Gestionnaire Personnalisé

**Fichier:** [Accounts/managers.py](Accounts/managers.py)

- `create_user()` - Création d'utilisateurs standards
- `create_superuser()` - Création d'administrateurs

### 3. Modèles de Profil

**Fichier:** [profiles/models.py](profiles/models.py)

#### StudentProfile
- student_id, level, group, speciality, department, address

#### TeacherProfile
- specialization, office, bio, rank, prefix, department

#### AdminProfile
- position, office, service, rank, department

### 4. Signaux de Création Automatique

**Fichier:** [profiles/signals.py](profiles/signals.py)

Crée automatiquement le profil approprié lors de la création d'un utilisateur en fonction de son rôle.

### 5. Formulaires

**Fichier:** [Accounts/forms.py](Accounts/forms.py)

- **UserRegistrationForm** - Inscription avec hashage du mot de passe
- **LoginForm** - Connexion par email/mot de passe

### 6. Vues

**Fichier:** [Accounts/views.py](Accounts/views.py)

- `register_view` - Inscription et redirection selon le rôle
- `login_view` - Authentification et redirection
- `logout_view` - Déconnexion
- `student_dashboard` - Tableau de bord étudiant (protégé)
- `teacher_dashboard` - Tableau de bord enseignant (protégé)
- `admin_dashboard` - Tableau de bord admin (protégé)

## 🌐 Routes Disponibles

### Routes Publiques
- `/` - Page d'accueil
- `/News/` - Actualités
- `/About_Us/` - À propos
- `/Contact_Us/` - Contact
- `/Accounts/login/` - Connexion
- `/Accounts/register/` - Inscription

### Routes Protégées (@login_required)
- `/Accounts/student/dashboard/` - Tableau de bord étudiant
- `/Accounts/teacher/dashboard/` - Tableau de bord enseignant
- `/Accounts/admin/dashboard/` - Tableau de bord admin

### Interface Admin
- `/admin/` - Interface d'administration Django

## ⚙️ Configuration

### settings.py

```python
INSTALLED_APPS = [
    # ...
    'Home',
    'Accounts',
    'profiles',
]

# Modèle utilisateur personnalisé
AUTH_USER_MODEL = "Accounts.User"

# URL de connexion
LOGIN_URL = '/Accounts/login/'
```

### URLs principales

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include('Home.urls')),
    path("Accounts/", include('Accounts.urls')),
]
```

## 🎨 Interface Utilisateur

### Navigation Dynamique

Le template de base affiche conditionnellement :
- **Utilisateur non connecté** : Boutons "Se connecter" et "S'inscrire"
- **Utilisateur connecté** : "Bonjour, [Prénom]" et bouton "Déconnexion"

### Tableaux de Bord par Rôle

Chaque rôle a un tableau de bord personnalisé avec des cartes d'action :

**Étudiant :**
- Mes Emprunts
- Mes Réservations
- Rechercher des livres
- Mon Profil

**Enseignant :**
- Mes Emprunts
- Catalogue
- Recommandations
- Mon Profil

**Administrateur :**
- Gestion des utilisateurs
- Gestion des livres
- Statistiques
- Configuration

## 🔐 Sécurité

### Protection des Vues

Utilisation du décorateur `@login_required` :

```python
@login_required
def student_dashboard(request):
    return render(request, "Accounts/student_dashboard.html")
```

### Hashage des Mots de Passe

Les mots de passe sont automatiquement hashés via `set_password()` :

```python
def save(self, commit=True):
    user = super().save(commit=False)
    user.set_password(self.cleaned_data["password"])
    if commit:
        user.save()
    return user
```

### Protection CSRF

Tous les formulaires incluent `{% csrf_token %}` pour la protection contre les attaques CSRF.

## 👤 Compte Admin par Défaut

**Email :** admin@bibliotheque.dz  
**Mot de passe :** admin123

## 📊 Interface d'Administration

### Fonctionnalités Admin

1. **Gestion des utilisateurs** avec profils inline
   - Affichage automatique du profil selon le rôle
   - Édition directe du profil dans la page utilisateur

2. **Filtres et recherche**
   - Recherche par email
   - Filtres par rôle, statut staff, statut actif

3. **Classes Admin pour les profils**
   - StudentProfileAdmin
   - TeacherProfileAdmin
   - AdminProfileAdmin

### Utilisation de l'Admin

```python
@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "student_id", "level", "group")
    search_fields = ("user__email", "student_id")
```

## 🚀 Utilisation

### 1. Créer un Nouvel Utilisateur

**Via l'interface web :**
1. Accédez à `/Accounts/register/`
2. Remplissez le formulaire
3. Sélectionnez le rôle
4. Soumettez

**Via l'admin Django :**
1. Accédez à `/admin/`
2. Allez dans "Users"
3. Cliquez sur "Add User"
4. Remplissez les informations
5. Le profil correspondant est créé automatiquement

### 2. Se Connecter

1. Accédez à `/Accounts/login/`
2. Entrez votre email et mot de passe
3. Vous serez redirigé vers le tableau de bord approprié

### 3. Gérer les Profils

1. Connectez-vous en tant qu'admin
2. Accédez à `/admin/`
3. Sélectionnez un utilisateur
4. Le profil correspondant s'affiche automatiquement
5. Modifiez les informations du profil

## 📝 Migrations

### Commandes Utilisées

```bash
# Créer les migrations
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate

# Créer un superutilisateur
python manage.py createsuperuser --email admin@bibliotheque.dz

# Vérifier le système
python manage.py check
```

## 🧪 Tests

### Scénarios à Tester

1. **Inscription**
   - Créer un compte étudiant
   - Créer un compte enseignant
   - Vérifier la création automatique du profil

2. **Connexion**
   - Se connecter avec un email valide
   - Tester avec un mot de passe incorrect
   - Vérifier la redirection selon le rôle

3. **Tableaux de Bord**
   - Accéder au dashboard sans connexion (doit rediriger)
   - Accéder au dashboard avec connexion
   - Vérifier les éléments affichés

4. **Administration**
   - Ajouter un utilisateur
   - Modifier un profil
   - Vérifier les filtres et recherches

## 🔄 Flux d'Authentification

```
1. Utilisateur → /Accounts/register/
2. Formulaire d'inscription
3. Validation des données
4. Création de User
5. Signal déclenché → Création automatique du profil
6. Connexion automatique
7. Redirection vers le dashboard approprié
```

## 📦 Dépendances

- Django 6.0.1
- Python 3.13
- SQLite (base de données par défaut)

## 🎯 Fonctionnalités Futures

- [ ] Reset de mot de passe par email
- [ ] Validation d'email
- [ ] Photos de profil
- [ ] Permissions granulaires
- [ ] Historique des connexions
- [ ] Authentification à deux facteurs
- [ ] API REST pour mobile

## 📚 Ressources

- [Documentation Django Auth](https://docs.djangoproject.com/en/6.0/topics/auth/)
- [Custom User Model](https://docs.djangoproject.com/en/6.0/topics/auth/customizing/)
- [Signals](https://docs.djangoproject.com/en/6.0/topics/signals/)

---

**Note :** Le système est maintenant complètement fonctionnel et prêt pour le développement de fonctionnalités supplémentaires !
