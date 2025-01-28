from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Book
from .forms import BookForm
from django.contrib import messages
from .forms import BookSearchForm

def is_librarian(user):
    return user.groups.filter(name='Librarian').exists()

@login_required
@user_passes_test(is_librarian)
def manage_books(request):
    # Your code to manage books goes here
    return render(request, 'books/manage_books.html')

@login_required
@user_passes_test(is_librarian)
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book added successfully!')
            return redirect('view_books')
    else:
        form = BookForm()
    return render(request, 'books/add_book.html', {'form': form})

@login_required
@user_passes_test(is_librarian)
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book updated successfully!')
            return redirect('view_books')
    else:
        form = BookForm(instance=book)
    return render(request, 'books/edit_book.html', {'form': form, 'book': book})

@login_required
@user_passes_test(is_librarian)
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    messages.success(request, 'Book deleted successfully!')
    return redirect('view_books')

@login_required
def view_books(request):
    books = Book.objects.all()
    
    # Filtering by genre or availability
    genre = request.GET.get('genre')
    status = request.GET.get('status')
    
    if genre:
        books = books.filter(genre=genre)
    if status:
        books = books.filter(status=status)

    return render(request, 'books/view_books.html', {'books': books})



def book_list(request):
    # Initialize the search form
    form = BookSearchForm(request.GET)
    books = Book.objects.all()

    if form.is_valid():
        search_term = form.cleaned_data['search_term']
        if search_term:
            # Filter books by title, author, or ISBN
            books = books.filter(
                title__icontains=search_term
            ) | books.filter(
                author__icontains=search_term
            ) | books.filter(
                isbn__icontains=search_term
            )
    
    return render(request, 'books/book_list.html', {'form': form, 'books': books})
