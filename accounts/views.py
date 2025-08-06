from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from django.template.defaultfilters import first
from django.views import View

from accounts.forms import LoginForm, RegisterForm, GroupForm, EditUserForm  # EditTeacherForm,
from school.conftest import subjects
from school.forms import AddSubjectToTeacherForm


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
        group_form = GroupForm()
        return render(request, 'form.html', {'form': [user_form, group_form], 'multiple' : True})

    def post(self, request):
        user_form = RegisterForm(request.POST)
        group_form = GroupForm(request.POST)
        if user_form.is_valid() and group_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password1'])
            group = Group.objects.get(name=group_form.cleaned_data['group'])
            user.save()
            user.groups.add(group)
            return redirect('home',)
        return render(request, 'form.html', {'form': [user_form, group_form], 'multiple' : True})

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
        form = EditUserForm(instance=user)
        return render(request, 'form.html', {'form': form})

    def post(self, request, pk):
        user = User.objects.get(pk=pk)
        form = EditUserForm(request.POST,instance=user)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            user.first_name = first_name
            user.last_name = last_name
            groups = form.cleaned_data['groups']
            user.groups.set(groups)
            return redirect('show_users')
        return render(request, 'form.html', {'form': form})


#TODO fix for current models
class AssignSubject(View):
    def get(self, request):
        form = AddSubjectToTeacherForm()
        return render(request, 'form.html', {'form': form})

    def post(self, request):
        form = AddSubjectToTeacherForm(request.POST)
        if form.is_valid():
            teacher = form.cleaned_data['teacher']
            subject = form.cleaned_data['subject']
            teacher.subject.set(subject)
            return redirect('home',)
        return render(request, 'form.html', {'form': form})

