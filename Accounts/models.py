# Accounts/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager


class User(AbstractUser):
    """Nous utilisons l'adresse e-mail comme identifiant de connexion."""
    username = None
    email = models.EmailField(unique=True)

    # Choix de rôles
    STUDENT = "student"
    TEACHER = "teacher"
    ADMIN = "admin"
    LIBRARIAN = "librarian"

    ROLE_CHOICES = [
        (STUDENT, "Étudiant"),
        (TEACHER, "Enseignant"),
        (ADMIN, "Admin"),
        (LIBRARIAN, "Bibliothécaire"),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=STUDENT)

    phone = models.CharField(max_length=20, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # Aucun nom d'utilisateur requis

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email} ({self.role})"


# Proxy models to expose role-specific listings in the admin
class StudentUser(User):
    class Meta:
        proxy = True
        verbose_name = "Étudiant"
        verbose_name_plural = "Étudiants"


class TeacherUser(User):
    class Meta:
        proxy = True
        verbose_name = "Enseignant"
        verbose_name_plural = "Enseignants"


class LibrarianUser(User):
    class Meta:
        proxy = True
        verbose_name = "Bibliothécaire"
        verbose_name_plural = "Bibliothécaires"
