from django.urls import path
from . import views

urlpatterns = [
    path('', views.manage_borrowing_records, name='manage_borrowing_records'),
    path('borrow/', views.borrow_book, name='borrow_book'),
    path('borrowed/', views.view_borrowed_books, name='view_borrowed_books'),
    path('borrow-requests/', views.view_borrow_requests, name='view_borrow_requests'),
    path('<int:record_id>/approve/', views.approve_borrowing, name='approve_borrowing'),
    path('<int:record_id>/reject/', views.reject_borrowing, name='reject_borrowing'),
    path('mark-returned/<int:borrow_id>/', views.mark_as_returned, name='mark_as_returned'),
]
