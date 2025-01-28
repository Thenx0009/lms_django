from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import BorrowRecord
from .forms import BorrowBookForm
from books.models import Book
from members.models import Member
from django.contrib import messages
from datetime import date

def is_librarian(user):
    return user.groups.filter(name='Librarian').exists()

from .utils import send_email_notification

@login_required
def borrow_book(request):
    if request.method == 'POST':
        form = BorrowBookForm(request.POST)
        if form.is_valid():
            borrow_record = form.save(commit=False)
            book = borrow_record.book
            if book.status == 'Available':
                book.status = 'Borrowed'
                book.save()
                borrow_record.save()

                # Send notification email to the member
                subject = 'Book Borrowed Successfully'
                message = f'You have borrowed the book: {borrow_record.book.title}. The due date is {borrow_record.due_date}.'
                send_email_notification(subject, message, [borrow_record.borrower.user.email])

                messages.success(request, 'Book borrowed successfully!')
                return redirect('view_borrowed_books')
            else:
                messages.error(request, 'The selected book is not available.')
    else:
        form = BorrowBookForm()

    return render(request, 'borrow/borrow_book.html', {'form': form})


@login_required
@user_passes_test(is_librarian)
def approve_borrow(request, borrow_id):
    borrow_record = get_object_or_404(BorrowRecord, id=borrow_id)
    if borrow_record.status == 'Pending':
        borrow_record.status = 'Approved'
        borrow_record.save()
        messages.success(request, 'Borrow request approved!')
    else:
        messages.error(request, 'This request has already been processed.')
    
    return redirect('view_borrow_requests')

@login_required
@user_passes_test(is_librarian)
def reject_borrow(request, borrow_id):
    borrow_record = get_object_or_404(BorrowRecord, id=borrow_id)
    if borrow_record.status == 'Pending':
        borrow_record.status = 'Rejected'
        borrow_record.save()
        # Set the book status back to 'Available'
        borrow_record.book.status = 'Available'
        borrow_record.book.save()
        messages.success(request, 'Borrow request rejected!')
    else:
        messages.error(request, 'This request has already been processed.')
    
    return redirect('view_borrow_requests')

@login_required
@user_passes_test(is_librarian)
def mark_as_returned(request, borrow_id):
    borrow_record = get_object_or_404(BorrowRecord, id=borrow_id)
    if borrow_record.status == 'Approved' and borrow_record.return_date is None:
        borrow_record.return_date = borrow_record.due_date  # Assuming book is returned on time
        borrow_record.status = 'Returned'
        borrow_record.book.status = 'Available'  # Update book status to available
        borrow_record.book.save()
        borrow_record.save()

        # Send notification email to the member
        subject = 'Book Returned Successfully'
        message = f'You have successfully returned the book: {borrow_record.book.title}. Thank you!'
        send_email_notification(subject, message, [borrow_record.borrower.user.email])

        messages.success(request, 'Book marked as returned.')
    else:
        messages.error(request, 'This book is not due or already returned.')
    
    return redirect('view_borrowed_books')

@login_required
def view_borrowed_books(request):
    member = get_object_or_404(Member, user=request.user)
    borrow_records = BorrowRecord.objects.filter(borrower=member).order_by('-borrow_date')

    # Check if any books are overdue and send reminders
    for record in borrow_records:
        if record.is_overdue() and record.status == 'Approved' and record.return_date is None:
            subject = 'Overdue Book Reminder'
            message = f'Your borrowed book "{record.book.title}" is overdue. Please return it as soon as possible.'
            send_email_notification(subject, message, [record.borrower.user.email])

    return render(request, 'borrow/view_borrowed_books.html', {'borrow_records': borrow_records})

@login_required
@user_passes_test(is_librarian)
def view_borrow_requests(request):
    borrow_records = BorrowRecord.objects.filter(status='Pending').order_by('-borrow_date')
    return render(request, 'borrow/view_borrow_requests.html', {'borrow_records': borrow_records})





