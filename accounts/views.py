from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View

from accounts.forms import LoginForm, RegisterForm


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
        form = RegisterForm()
        return render(request, 'form.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('home',)
        return render(request, 'form.html', {'form': form})