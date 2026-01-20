# Accounts/urls.py

from django.urls import path
from .views import (
    login_view,
    logout_view,
    register_view,
    admin_dashboard,
    edit_user,
    delete_user,
)

app_name = "accounts"

urlpatterns = [
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("register/", register_view, name="register"),
    path("admin/dashboard/", admin_dashboard, name="admin_dashboard"),
    path("admin/user/<int:pk>/edit/", edit_user, name="edit_user"),
    path("admin/user/<int:pk>/delete/", delete_user, name="delete_user"),
]
