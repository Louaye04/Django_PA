# Accounts/forms.py

from django import forms
from .models import User


class UserRegistrationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Exclure le rôle 'admin' du choix disponible lors de l'inscription
        if 'role' in self.fields:
            self.fields['role'].choices = [c for c in self.fields['role'].choices if c[0] != User.ADMIN]

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'role']
        labels = {
            'first_name': 'Prénom',
            'last_name': 'Nom de famille',
            'email': 'Adresse e-mail',
            'password': 'Mot de passe',
            'role': 'Rôle',
        }
        widgets = {
            'password': forms.PasswordInput(),
            'role': forms.Select(),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  # Hacher le mot de passe
        if commit:
            user.save()
        return user


class UserEditForm(forms.ModelForm):
    """Formulaire d'édition d'un utilisateur depuis le dashboard admin du site.

    Le champ `password` est optionnel : s'il est fourni, on met à jour le mot de passe.
    """
    password = forms.CharField(label='Mot de passe', widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'role']
        widgets = {
            'role': forms.Select(),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        pwd = self.cleaned_data.get('password')
        if pwd:
            user.set_password(pwd)
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField(label='Adresse e-mail')
    password = forms.CharField(label='Mot de passe', widget=forms.PasswordInput)
