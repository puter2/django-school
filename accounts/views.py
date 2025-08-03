from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.template.defaultfilters import first
from django.views import View

from accounts.forms import LoginForm, RegisterForm, RoleForm, EditTeacherForm
from accounts.models import Role
from school.conftest import subjects
from school.forms import AddSubjectToTeacherForm
from school.models import Teacher


# Create your views here.

class LoginView(View):

    def get(self, request):
        form = LoginForm()
        return render(request, 'form.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return render(request, 'base.html', {'message': 'logged in'})
        return render(request, 'form.html', {'message': 'error'})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')

class RegisterView(View):
    def get(self, request):
        user_form = RegisterForm()
        role_form = RoleForm()
        return render(request, 'form.html', {'form': [user_form, role_form], 'multiple' : True})

    def post(self, request):
        user_form = RegisterForm(request.POST)
        role_form = RoleForm(request.POST)
        if user_form.is_valid() and role_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password1'])
            user.save()
            role = Role.objects.create(user=user, role=role_form.cleaned_data['role'])
            return redirect('home',)
        return render(request, 'form.html', {'form': [user_form, role_form], 'multiple' : True})

class DeleteUserView(View):
    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        return render(request, 'delete_form.html', {'obj_name': user})

    def post(self, request, pk):
        if request.POST.get('operation') == 'Yes':
            user = User.objects.get(pk=pk)
            user.delete()
        return redirect('show_users')

class EditUserView(View):
    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        form = EditTeacherForm(instance=user)
        return render(request, 'form.html', {'form': form})

    def post(self, request, pk):
        user = User.objects.get(pk=pk)
        form = EditTeacherForm(request.POST,instance=user)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            user.first_name = first_name
            user.last_name = last_name
            if user.role.role == 'teacher':
                subjects = form.cleaned_data['subject']
                Teacher.objects.get(user=user).subject.set(subjects)
            return redirect('show_users')
        return render(request, 'form.html', {'form': form})

