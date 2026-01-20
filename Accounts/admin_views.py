from django.contrib import admin, messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User
from .forms import UserRegistrationForm


@admin.site.admin_view
def manage_accounts(request):
    """Vue d'administration personnalisée pour gérer les comptes par rôle.

    GET: affiche le formulaire de création et la liste filtrable/paginée.
    POST: crée un nouvel utilisateur via `UserRegistrationForm`.
    """
    q = request.GET.get("q", "").strip()
    role = request.GET.get("role", "all")

    # Traitement du formulaire de création (colonne de gauche)
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"Compte créé: {user.email}")
            return redirect(request.path)
        else:
            messages.error(request, "Veuillez corriger les erreurs du formulaire.")
    else:
        form = UserRegistrationForm()

    # Requête principale pour la liste (colonne de droite)
    users = User.objects.all().order_by("-created_at")
    # Exclure les comptes d'administration du listing
    users = users.exclude(role=User.ADMIN)
    if role in (User.STUDENT, User.TEACHER, User.LIBRARIAN):
        users = users.filter(role=role)

    if q:
        users = users.filter(
            email__icontains=q
        )

    paginator = Paginator(users, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Construire URL d'édition/suppression via le namespace admin
    def admin_change_url(obj):
        return reverse(
            f"admin:{obj._meta.app_label}_{obj._meta.model_name}_change",
            args=[obj.pk],
        )

    def admin_delete_url(obj):
        return reverse(
            f"admin:{obj._meta.app_label}_{obj._meta.model_name}_delete",
            args=[obj.pk],
        )

    context = {
        "title": "Gestion des Comptes",
        "form": form,
        "page_obj": page_obj,
        "q": q,
        "role": role,
        "admin_change_url": admin_change_url,
        "admin_delete_url": admin_delete_url,
    }

    return render(request, "admin/accounts_manage.html", context)
