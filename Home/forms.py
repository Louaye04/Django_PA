from django import forms
from .models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'genre', 'availability', 'quantity', 'cover', 'description']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Titre du livre',
                'id': 'id_title'
            }),
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Auteur',
                'id': 'id_author'
            }),
            'genre': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_genre'
            }),
            'availability': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_availability'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'id': 'id_quantity',
                'min': '1',
                'placeholder': '1'
            }),
            'cover': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'id': 'id_cover'
            }),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'id': 'id_description'}),
        }
