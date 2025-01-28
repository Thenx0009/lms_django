from django import forms
from .models import BorrowRecord
from books.models import Book
from members.models import Member

class BorrowBookForm(forms.ModelForm):
    class Meta:
        model = BorrowRecord
        fields = ['book', 'borrower', 'due_date']
    
    book = forms.ModelChoiceField(queryset=Book.objects.filter(status='Available'), empty_label="Select Book")
    borrower = forms.ModelChoiceField(queryset=Member.objects.all(), empty_label="Select Borrower")
    due_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
