from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Member
from .forms import MemberForm
from borrow.models import BorrowRecord
from django.contrib.auth.models import Group
from .forms import UserRegistrationForm, RoleForm
from django.contrib import messages


# Registration View
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        role_form = RoleForm(request.POST)
        if user_form.is_valid() and role_form.is_valid():
            user = user_form.save()
            role = role_form.cleaned_data['role']

            # Assign user to role group
            group = Group.objects.get(name=role)
            user.groups.add(group)

            messages.success(request, f'Account created successfully as {role}!')
            return redirect('login')  # Redirect to login page or home
    else:
        user_form = UserRegistrationForm()
        role_form = RoleForm()

    return render(request, 'members/register.html', {'user_form': user_form, 'role_form': role_form})


# Check if the user is a librarian
def is_librarian(user):
    return user.groups.filter(name='Librarian').exists()


# Add Member View (Librarian Only)
@login_required
@user_passes_test(is_librarian)
def add_member(request):
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Member added successfully!')
            return redirect('view_members')
    else:
        form = MemberForm()
    return render(request, 'members/add_member.html', {'form': form})


# View Members (Librarian Only)
@login_required
@user_passes_test(is_librarian)
def view_members(request):
    members = Member.objects.all()
    return render(request, 'members/view_members.html', {'members': members})


# View Borrow History (Member Only)
@login_required
def view_borrow_history(request):
    member = get_object_or_404(Member, user=request.user)
    borrow_history = BorrowRecord.objects.filter(borrower=member).order_by('-borrow_date')
    return render(request, 'members/borrow_history.html', {'borrow_history': borrow_history})


# List All Members (No Authentication)
def member_list(request):
    members = Member.objects.all()  # Fetch all members from the database
    return render(request, 'members/member_list.html', {'members': members})
