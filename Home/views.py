from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required

from .models import Book
from .forms import BookForm


def index(request):
    return render(request, 'Home/index.html')


def about_us(request):
    return render(request, 'Home/About_Us.html')


def contact_us(request):
    return render(request, 'Home/Contact_Us.html')


def news(request):
    return render(request, 'Home/News.html')


def manage_books(request):
    """Interface simple pour que le bibliothécaire gère le catalogue de livres."""
    q = request.GET.get('q', '').strip()
    genre = request.GET.get('genre', 'all')

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Livre ajouté avec succès.')
            return redirect(request.path)
        else:
            messages.error(request, 'Veuillez corriger les erreurs du formulaire.')
    else:
        form = BookForm()

    books = Book.objects.all()
    if genre != 'all':
        books = books.filter(genre=genre)

    if q:
        books = books.filter(title__icontains=q) | books.filter(author__icontains=q)

    paginator = Paginator(books, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    def site_change_url(obj):
        return reverse("edit_book", args=[obj.pk])

    def site_delete_url(obj):
        return reverse("delete_book", args=[obj.pk])

    # Préparer les lignes avec URLs (les templates Django ne peuvent pas appeler des fonctions)
    rows = []
    for b in page_obj.object_list:
        rows.append({
            'book': b,
            'change_url': site_change_url(b),
            'delete_url': site_delete_url(b),
        })

    context = {
        'title': 'Gestion des livres',
        'form': form,
        'page_obj': page_obj,
        'rows': rows,
        'q': q,
        'genre': genre,
        'genres': Book.GENRE_CHOICES,
    }
    # Allow selecting a specific favicon and page title depending on section (catalogue/commandes/emprunts)
    section = request.GET.get('section', '').lower()
    if section == 'commandes' or section == 'orders':
        context['page_favicon'] = 'Home/favicon_commandes.svg'
        context['page_title'] = '📚 Commandes des adhérents — Bibliothèque Universitaire'
    elif section == 'emprunts' or section == 'loans':
        context['page_favicon'] = 'Home/favicon_emprunts.svg'
        context['page_title'] = '📚 Emprunts des adhérents — Bibliothèque Universitaire'
    else:
        # default to catalogue favicon / title
        context['page_favicon'] = 'Home/favicon_catalogue.svg'
        context['page_title'] = '📚 Catalogue (Bibliothécaire) — Bibliothèque Universitaire'

    return render(request, 'Home/library_manage.html', context)


def edit_book(request, pk):
    from .models import Book
    from .forms import BookForm
    book = get_object_or_404(Book, pk=pk)
    # permission: only librarians or staff
    user = request.user
    role = getattr(user, 'role', '')
    if not (user.is_staff or user.is_superuser or 'librarian' in str(role).lower()):
        messages.error(request, "Accès refusé.")
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.GET.get('ajax'):
            if not user.is_authenticated:
                return JsonResponse({'success': False, 'login_required': True, 'login_url': settings.LOGIN_URL}, status=401)
            return JsonResponse({'success': False, 'forbidden': True, 'message': 'Accès refusé.'}, status=403)
        return redirect('manage_books')

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Livre mis à jour.')
            # If AJAX POST, return JSON success
            if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.POST.get('ajax'):
                return JsonResponse({'success': True})
            return redirect('manage_books')
        else:
            messages.error(request, 'Veuillez corriger les erreurs du formulaire.')
            if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.POST.get('ajax'):
                html = render_to_string('Home/partials/book_form.html', {'form': form, 'book': book}, request=request)
                return JsonResponse({'success': False, 'html': html})
    else:
        form = BookForm(instance=book)

    # If AJAX request, return rendered form fragment
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.GET.get('ajax'):
        html = render_to_string('Home/partials/book_form.html', {'form': form, 'book': book}, request=request)
        return JsonResponse({'html': html})

    return render(request, 'Home/edit_book.html', {'form': form, 'book': book})


def delete_book(request, pk):
    from .models import Book
    book = get_object_or_404(Book, pk=pk)
    user = request.user
    role = getattr(user, 'role', '')
    if not (user.is_staff or user.is_superuser or 'librarian' in str(role).lower()):
        messages.error(request, "Accès refusé.")
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.GET.get('ajax'):
            if not user.is_authenticated:
                return JsonResponse({'success': False, 'login_required': True, 'login_url': settings.LOGIN_URL}, status=401)
            return JsonResponse({'success': False, 'forbidden': True, 'message': 'Accès refusé.'}, status=403)
        return redirect('manage_books')

    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Livre supprimé.')
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.POST.get('ajax'):
            return JsonResponse({'success': True})
        return redirect('manage_books')

    # For safety, render a small confirmation fragment
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.GET.get('ajax'):
        html = render_to_string('Home/partials/confirm_delete.html', {'book': book}, request=request)
        return JsonResponse({'html': html})

    return render(request, 'Home/confirm_delete.html', {'book': book})
