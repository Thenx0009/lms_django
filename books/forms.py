from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'genre', 'publication_year', 'isbn', 'status']


class BookSearchForm(forms.Form):
    search_term = forms.CharField(
        label='Search by Title, Author, or ISBN',
        max_length=100,
        required=False
    )
