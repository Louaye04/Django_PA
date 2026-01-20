# Accounts/managers.py

from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, role=None, **extra_fields):
        """Créer et renvoyer un utilisateur standard avec une adresse e-mail et un mot de passe."""
        if not email:
            raise ValueError("Les utilisateurs doivent avoir une adresse e-mail")

        email = self.normalize_email(email)

        # Rôle par défaut si non fourni
        if role is None:
            role = self.model.STUDENT

        user = self.model(email=email, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Créer et renvoyer un superutilisateur avec le rôle ADMIN."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Le superutilisateur doit avoir is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Le superutilisateur doit avoir is_superuser=True.")

        return self.create_user(
            email=email,
            password=password,
            role=self.model.ADMIN,
            **extra_fields,
        )
