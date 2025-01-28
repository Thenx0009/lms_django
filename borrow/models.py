from django.db import models
from django.contrib.auth.models import User
from books.models import Book
from members.models import Member

class BorrowRecord(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Returned', 'Returned'),
    ]
    
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrower = models.ForeignKey(Member, on_delete=models.CASCADE)
    borrow_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.book.title} - {self.borrower.user.username} - {self.status}"

    def is_overdue(self):
        from datetime import date
        return self.status == 'Approved' and self.due_date < date.today()
