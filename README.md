# 📚 Site Web de Gestion de Bibliothèque Universitaire

Un système complet de gestion de bibliothèque développé avec Django, HTML, CSS et JavaScript.

## 🎯 Caractéristiques

### Interface Utilisateur
- Interface moderne et responsive
- Page d'accueil avec présentation de la bibliothèque
- Section actualités
- Page à propos
- Formulaire de contact
- Design professionnel avec dégradés et animations

### Système d'Authentification
- **Trois types de rôles** : Étudiant, Enseignant, Administrateur
- Inscription et connexion sécurisées
- Tableaux de bord personnalisés par rôle
- Gestion des profils utilisateurs
- Protection des routes avec @login_required
- Interface d'administration Django complète

## 🚀 Installation et Configuration

### 1. Créer l'environnement virtuel

```bash
python -m venv UniversityPlatformEnv
```

### 2. Activer l'environnement virtuel

**Sous Windows :**
```bash
UniversityPlatformEnv\Scripts\activate
```

**Sur macOS/Linux :**
```bash
source UniversityPlatformEnv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Créer la base de données

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Créer un superutilisateur

```bash
python manage.py createsuperuser
```

### 6. Lancer le serveur de développement

```bash
python manage.py runserver
```

Accédez ensuite à : http://localhost:8000

## � Compte Admin par Défaut

**Email :** admin@bibliotheque.dz  
**Mot de passe :** admin123

Accédez à l'interface admin : http://localhost:8000/admin

## 📁 Structure du Projet

```
django_bib/
├── University_Platform/        # Configuration du projet Django
│   ├── settings.py            # Paramètres du projet (AUTH_USER_MODEL configuré)
│   ├── urls.py                # Routes principales
│   └── wsgi.py                # Interface WSGI
│
├── Accounts/                  # Application de gestion des comptes
│   ├── managers.py            # Gestionnaire d'utilisateurs personnalisé
│   ├── models.py              # Modèle User personnalisé
│   ├── forms.py               # Formulaires d'inscription/connexion
│   ├── views.py               # Vues d'authentification
│   ├── urls.py                # Routes de l'application
│   ├── admin.py               # Configuration admin
│   └── templates/Accounts/    # Templates d'authentification
│       ├── register.html      # Formulaire d'inscription
│       ├── login.html         # Formulaire de connexion
│       ├── student_dashboard.html
│       ├── teacher_dashboard.html
│       └── admin_dashboard.html
│
├── profiles/                  # Application des profils utilisateurs
│   ├── models.py              # Modèles StudentProfile, TeacherProfile, AdminProfile
│   ├── signals.py             # Création automatique des profils
│   ├── apps.py                # Configuration avec signaux
│   └── admin.py               # Administration des profils
│
├── Home/                      # Application Home
│   ├── templates/             # Templates HTML
│   │   └── Home/
│   │       ├── base_Home.html       # Template de base
│   │       ├── index.html           # Page d'accueil
│   │       ├── News.html            # Page actualités
│   │       ├── About_Us.html        # Page à propos
│   │       └── Contact_Us.html      # Page contact
│   │
│   ├── static/                # Fichiers statiques
│   │   └── Home/
│   │       └── CSS/
│   │           └── styles.css       # Styles CSS
│   │
│   ├── views.py               # Vues de l'application
│   ├── urls.py                # Routes de l'application
│   └── models.py              # Modèles de données
│
├── db.sqlite3                 # Base de données SQLite
└── manage.py                  # Utilitaire de gestion Django
```

## 🎨 Pages Disponibles

### Pages Publiques
1. **Accueil** (`/`) - Page d'accueil avec présentation des services
2. **Actualités** (`/News/`) - Dernières nouvelles de la bibliothèque
3. **À propos** (`/About_Us/`) - Informations sur la bibliothèque
4. **Contact** (`/Contact_Us/`) - Formulaire de contact
5. **Connexion** (`/Accounts/login/`) - Authentification
6. **Inscription** (`/Accounts/register/`) - Création de compte

### Pages Protégées (Login Requis)
1. **Dashboard Étudiant** (`/Accounts/student/dashboard/`)
2. **Dashboard Enseignant** (`/Accounts/teacher/dashboard/`)
3. **Dashboard Administrateur** (`/Accounts/admin/dashboard/`)

### Interface Admin
- **Administration Django** (`/admin/`) - Gestion complète du système

## 💻 Technologies Utilisées

- **Backend:** Django 6.0.1
- **Frontend:** HTML5, CSS3, JavaScript
- **Base de données:** SQLite
- **Python:** 3.13
- **Authentification:** Django Auth avec modèle User personnalisé

## 📝 Configuration

Le fichier `settings.py` contient toutes les configurations du projet :

- `AUTH_USER_MODEL = "Accounts.User"` : Modèle utilisateur personnalisé
- `LOGIN_URL = '/Accounts/login/'` : URL de redirection pour les pages protégées

- `INSTALLED_APPS` : Liste des applications installées
- `STATIC_URL` : URL des fichiers statiques
- `DEBUG` : Mode debug (True en développement)

## 🔧 Commandes Utiles

### Créer un superutilisateur (admin)
```bash
python manage.py createsuperuser
```

### Accéder à l'interface admin
http://localhost:8000/admin

### Créer une nouvelle application
```bash
python manage.py startapp nom_app
```

### Créer des migrations
```bash
python manage.py makemigrations
```

### Appliquer les migrations
```bash
python manage.py migrate
```

## 🎓 Fonctionnalités Implémentées

- [x] Système d'authentification complet (login/register)
- [x] Trois types de rôles utilisateurs
- [x] Gestion des profils utilisateurs
- [x] Tableaux de bord personnalisés
- [x] Interface d'administration Django
- [x] Protection des routes avec @login_required
- [x] Création automatique des profils via signaux

## 🎯 Fonctionnalités Futures

- [ ] Gestion du catalogue de livres
- [ ] Système d'emprunt et de retour
- [ ] Réservation de livres
- [ ] Recherche avancée dans le catalogue
- [ ] Historique des emprunts
- [ ] Notifications par email
- [ ] Export de données
- [ ] Reset de mot de passe
- [ ] Upload de photos de profil

## 📖 Documentation Complète

Pour une documentation détaillée du système d'authentification, consultez :
- [AUTHENTICATION_GUIDE.md](AUTHENTICATION_GUIDE.md) - Guide complet du système de gestion des comptes

## 📄 License

Ce projet est développé à des fins éducatives.

## 👨‍💻 Auteur

Projet développé pour la gestion d'une bibliothèque universitaire.

---

**Note:** Assurez-vous d'avoir Python 3.8+ installé sur votre système.
