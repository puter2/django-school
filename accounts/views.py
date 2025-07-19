from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View

from accounts.forms import LoginForm, RegisterForm, RoleForm


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
            role = role_form.save(commit=False)
            role.user = user
            user.set_password(user_form.cleaned_data['password1'])
            user.save()
            role.save()
            return redirect('home',)
        return render(request, 'form.html', {'form': [user_form, role_form], 'multiple' : True})