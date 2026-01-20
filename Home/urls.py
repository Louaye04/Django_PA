"""Définit les modèles d'URL pour l'application Accueil."""
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('News/', views.news, name='News'),
    path('About_Us/', views.about_us, name='About_Us'),
    path('Contact_Us/', views.contact_us, name='Contact_Us'),
    path('librarian/books/', views.manage_books, name='manage_books'),
    path('librarian/book/<int:pk>/edit/', views.edit_book, name='edit_book'),
    path('librarian/book/<int:pk>/delete/', views.delete_book, name='delete_book'),
]
