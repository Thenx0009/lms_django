from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.member_list, name='member_list'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('add/', views.add_member, name='add_member'),
    path('view/', views.view_members, name='view_members'),
    path('borrow-history/', views.view_borrow_history, name='borrow_history'),
]
