# Script de Test du Système d'Authentification

Ce fichier documente comment tester toutes les fonctionnalités du système.

## 🧪 Tests Manuels

### 1. Test d'Inscription

#### Étape 1 : Accéder à la page d'inscription
- URL : http://localhost:8000/Accounts/register/
- Vérifier que le formulaire s'affiche correctement

#### Étape 2 : Créer un compte étudiant
- Prénom : Jean
- Nom : Dupont
- Email : jean.dupont@student.dz
- Téléphone : 0555123456
- Mot de passe : student123
- Rôle : Étudiant
- Cliquer sur "S'inscrire"

#### Résultat attendu :
- Redirection vers `/Accounts/student/dashboard/`
- Message de bienvenue avec le prénom
- Affichage des cartes du tableau de bord étudiant

### 2. Test de Connexion

#### Étape 1 : Se déconnecter
- Cliquer sur "Déconnexion" dans la barre de navigation

#### Étape 2 : Se reconnecter
- URL : http://localhost:8000/Accounts/login/
- Email : jean.dupont@student.dz
- Mot de passe : student123
- Cliquer sur "Se connecter"

#### Résultat attendu :
- Redirection vers le dashboard étudiant
- Session active

### 3. Test des Rôles

#### Créer un Enseignant
- URL : http://localhost:8000/Accounts/register/
- Email : prof.martin@teacher.dz
- Rôle : Enseignant
- Mot de passe : teacher123

**Résultat attendu :** Dashboard enseignant

#### Créer un Admin
- Via l'interface admin : http://localhost:8000/admin/
- Se connecter avec : admin@bibliotheque.dz / admin123
- Créer un utilisateur avec rôle "Admin"

**Résultat attendu :** Dashboard administrateur

### 4. Test de Protection des Routes

#### Tester l'accès sans connexion
- Se déconnecter
- Essayer d'accéder à : http://localhost:8000/Accounts/student/dashboard/

**Résultat attendu :** Redirection vers `/Accounts/login/`

### 5. Test de l'Interface Admin

#### Accéder à l'admin
- URL : http://localhost:8000/admin/
- Login : admin@bibliotheque.dz
- Password : admin123

#### Vérifier les fonctionnalités :
- [ ] Liste des utilisateurs affichée
- [ ] Filtres fonctionnels (rôle, staff, actif)
- [ ] Recherche par email
- [ ] Édition d'un utilisateur
- [ ] Profil inline affiché selon le rôle

### 6. Test des Profils Automatiques

#### Dans l'admin Django :
1. Créer un nouvel utilisateur avec rôle "Étudiant"
2. Sauvegarder
3. Éditer l'utilisateur
4. Vérifier que "Profil de l'étudiant" s'affiche automatiquement
5. Remplir les champs du profil :
   - Student ID : STU2026001
   - Level : L3
   - Group : G01
   - Speciality : Informatique
   - Department : Sciences et Technologies

**Résultat attendu :** Profil créé automatiquement et modifiable

### 7. Test de la Navigation Dynamique

#### Utilisateur non connecté :
- Vérifier affichage : "Se connecter | S'inscrire"

#### Utilisateur connecté :
- Vérifier affichage : "Bonjour, [Prénom] | Déconnexion"

## 🔍 Tests à effectuer dans l'ordre

1. ✅ Inscription d'un étudiant
2. ✅ Connexion avec cet étudiant
3. ✅ Vérification du dashboard étudiant
4. ✅ Déconnexion
5. ✅ Inscription d'un enseignant
6. ✅ Vérification du dashboard enseignant
7. ✅ Connexion en tant qu'admin
8. ✅ Création d'utilisateur via l'admin
9. ✅ Vérification du profil automatique
10. ✅ Test de protection des routes

## 📊 Résultats Attendus

### Base de données
- Table `Accounts_user` : 3+ utilisateurs
- Table `profiles_studentprofile` : 1+ profil
- Table `profiles_teacherprofile` : 1+ profil
- Table `profiles_adminprofile` : 1+ profil

### Fonctionnalités
- ✅ Inscription fonctionnelle
- ✅ Connexion fonctionnelle
- ✅ Déconnexion fonctionnelle
- ✅ Redirection par rôle fonctionnelle
- ✅ Protection des routes fonctionnelle
- ✅ Création automatique des profils fonctionnelle
- ✅ Interface admin fonctionnelle

## 🐛 Cas d'Erreur à Tester

### 1. Inscription avec email existant
- Créer un compte avec un email déjà utilisé
- **Attendu :** Message d'erreur

### 2. Connexion avec mauvais mot de passe
- Email : jean.dupont@student.dz
- Mot de passe : wrongpassword
- **Attendu :** Message "Adresse e-mail ou mot de passe invalide"

### 3. Connexion avec email inexistant
- Email : inexistant@test.dz
- **Attendu :** Message d'erreur

### 4. Champs obligatoires vides
- Soumettre le formulaire d'inscription sans remplir les champs
- **Attendu :** Messages de validation

## 📝 Commandes de Vérification

### Vérifier les utilisateurs créés
```bash
python manage.py shell
```

```python
from Accounts.models import User
from profiles.models import StudentProfile, TeacherProfile, AdminProfile

# Lister tous les utilisateurs
for user in User.objects.all():
    print(f"{user.email} - {user.role}")

# Vérifier les profils
print(f"Étudiants: {StudentProfile.objects.count()}")
print(f"Enseignants: {TeacherProfile.objects.count()}")
print(f"Admins: {AdminProfile.objects.count()}")
```

### Vérifier la base de données
```bash
python manage.py dbshell
```

```sql
SELECT * FROM Accounts_user;
SELECT * FROM profiles_studentprofile;
SELECT * FROM profiles_teacherprofile;
SELECT * FROM profiles_adminprofile;
```

## ✅ Checklist Complète

- [ ] Page d'accueil accessible
- [ ] Page d'inscription fonctionnelle
- [ ] Page de connexion fonctionnelle
- [ ] Dashboard étudiant accessible après connexion
- [ ] Dashboard enseignant accessible après connexion
- [ ] Dashboard admin accessible après connexion
- [ ] Déconnexion fonctionnelle
- [ ] Redirection vers login pour pages protégées
- [ ] Navigation affiche le nom de l'utilisateur connecté
- [ ] Interface admin accessible
- [ ] Création d'utilisateur via admin
- [ ] Profils créés automatiquement
- [ ] Profils modifiables dans l'admin
- [ ] Filtres et recherche dans l'admin fonctionnels

## 🎉 Succès !

Si tous les tests passent, le système d'authentification est complètement fonctionnel !
