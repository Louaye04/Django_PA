# Accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.urls import reverse
from datetime import datetime
from .forms import UserRegistrationForm, LoginForm
from .models import User
from .forms import UserEditForm
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST


def register_view(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Bienvenue {user.first_name} ! Votre compte {user.get_role_display()} a été créé avec succès.")
            return redirect("index")
        else:
            return render(request, "Accounts/register.html", {"form": form})
    else:
        form = UserRegistrationForm()
    return render(request, "Accounts/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Bienvenue {user.first_name} ! Vous êtes connecté en tant que {user.get_role_display()}.")
                # Trace minimale dans un fichier pour debug de redirection
                try:
                    with open('login_debug.log', 'a', encoding='utf-8') as _f:
                        _f.write(f"{datetime.utcnow().isoformat()} | LOGIN attempt | email={email} | role={getattr(user,'role',None)} | display={user.get_role_display()} | is_staff={user.is_staff} | is_super={user.is_superuser}\n")
                except Exception:
                    pass
                # Respecter un paramètre `next` interne si présent
                next_url = request.POST.get('next') or request.GET.get('next')
                if next_url and str(next_url).startswith('/'):
                    return redirect(next_url)

                # Prioriser la redirection vers l'interface bibliothécaire.
                # Utiliser une détection tolérante au cas où la valeur serait différente
                user_role = getattr(user, "role", "") or ""
                role_display = (user.get_role_display() or "")
                is_librarian = False
                try:
                    if str(user_role).lower() == str(User.LIBRARIAN).lower():
                        is_librarian = True
                except Exception:
                    pass
                if not is_librarian:
                    # essayer d'identifier via le libellé affiché
                    if 'biblioth' in str(role_display).lower() or 'librarian' in str(role_display).lower():
                        is_librarian = True

                if is_librarian:
                    return redirect('/librarian/books/')

                # Si l'utilisateur a le rôle admin, l'envoyer vers le dashboard admin
                if getattr(user, "role", None) == User.ADMIN or user.is_staff or user.is_superuser:
                    return redirect("accounts:admin_dashboard")

                return redirect("index")
            else:
                messages.error(request, "Adresse e-mail ou mot de passe invalide")
        else:
            messages.error(request, "Adresse e-mail ou mot de passe invalide")
    else:
        form = LoginForm()
    # Fournir un titre de page explicite pour l'onglet du navigateur
    return render(request, "Accounts/login.html", {"form": form, "page_title": "📚 Connexion — Bibliothèque Universitaire"})


def logout_view(request):
    logout(request)
    # Ne pas créer de message flash à la déconnexion — rediriger directement vers la page de login
    return redirect("accounts:login")


@login_required
def admin_dashboard(request):
    """Vue dashboard pour les administrateurs produisant la même UX de gestion des comptes.

    Autorise uniquement les utilisateurs avec `role == 'admin'` ou `is_staff`.
    """
    user = request.user
    if not (getattr(user, "role", None) == User.ADMIN or user.is_staff or user.is_superuser):
        messages.error(request, "Accès refusé : vous n'êtes pas administrateur.")
        return redirect("index")

    q = request.GET.get("q", "").strip()
    role = request.GET.get("role", "all")

    # Traitement du formulaire de création (colonne de gauche)
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            messages.success(request, f"Compte créé: {new_user.email}")
            return redirect(request.path)
        else:
            messages.error(request, "Veuillez corriger les erreurs du formulaire.")
    else:
        form = UserRegistrationForm()

    users = User.objects.all().order_by("-created_at")
    # Exclure les comptes d'administration du listing
    users = users.exclude(role=User.ADMIN)
    if role in (User.STUDENT, User.TEACHER, User.LIBRARIAN):
        users = users.filter(role=role)

    if q:
        users = users.filter(email__icontains=q)

    paginator = Paginator(users, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Pré-calculer les URLs d'édition/suppression côté site (pas l'admin Django)
    rows = []
    for u in page_obj.object_list:
        rows.append({
            "user": u,
            "change_url": reverse("accounts:edit_user", args=[u.pk]),
            "delete_url": reverse("accounts:delete_user", args=[u.pk]),
        })

    context = {
        "title": "Dashboard Administrateur",
        "form": form,
        "page_obj": page_obj,
        "rows": rows,
        "q": q,
        "role": role,
        "User": User,
    }

    return render(request, "Accounts/admin_dashboard.html", context)


@login_required
def edit_user(request, pk):
    user = request.user
    if not (getattr(user, "role", None) == User.ADMIN or user.is_staff or user.is_superuser):
        messages.error(request, "Accès refusé : vous n'êtes pas administrateur.")
        return redirect("index")

    target = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        form = UserEditForm(request.POST, instance=target)
        if form.is_valid():
            form.save()
            messages.success(request, "Utilisateur mis à jour.")
            return redirect(reverse("accounts:admin_dashboard"))
        else:
            messages.error(request, "Veuillez corriger les erreurs du formulaire.")
    else:
        form = UserEditForm(instance=target)

    return render(request, "Accounts/edit_user.html", {"form": form, "target": target})


@login_required
@require_POST
def delete_user(request, pk):
    user = request.user
    if not (getattr(user, "role", None) == User.ADMIN or user.is_staff or user.is_superuser):
        messages.error(request, "Accès refusé : vous n'êtes pas administrateur.")
        return redirect("index")

    target = get_object_or_404(User, pk=pk)
    # Empêcher la suppression de soi-même
    if target.pk == user.pk:
        messages.error(request, "Vous ne pouvez pas supprimer votre propre compte.")
        return redirect(reverse("accounts:admin_dashboard"))

    target.delete()
    messages.success(request, "Utilisateur supprimé.")
    return redirect(reverse("accounts:admin_dashboard"))
