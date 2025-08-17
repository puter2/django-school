from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from django.template.defaultfilters import first
from django.utils.archive import extract
from django.views import View

from accounts.forms import LoginForm, RegisterForm, GroupForm, EditUserForm  # EditTeacherForm,
from school.forms import AddSubjectToTeacherForm, CreateClassForm, AddSubjectForm, EditStudentClassForm
from school.models import Subject, Klass


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
        print(group_form)
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
        extra_form = None
        if user.groups.all()[0].name == 'Teachers':
            extra_form = AddSubjectToTeacherForm(teacher=user)
        elif user.groups.all()[0].name == 'Students':
            extra_form = EditStudentClassForm(student=user)
        forms = [form, extra_form]
        return render(request, 'form.html', {'form': forms, 'multiple' : True})
    def post(self, request, pk):
        user = User.objects.get(pk=pk)
        form = EditUserForm(request.POST,instance=user)
        if user.groups.all()[0].name == 'Teachers':
            #TODO teacher side
            #TODO admin?
            extra_form = AddSubjectToTeacherForm(request.POST, student=user)
        else:
            extra_form = EditStudentClassForm(request.POST, student=user)
        print(extra_form.errors)
        if form.is_valid() and extra_form.is_valid():
            print('a')
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            user.first_name = first_name
            user.last_name = last_name
            groups = form.cleaned_data['groups']
            user.groups.set(groups)
            user.save()

            if user.groups.all()[0].name == 'Teachers':
                selected_subjects = extra_form.cleaned_data['subject']
                print(selected_subjects)
                teacher_subject = Subject.objects.filter(teacher=user)
                for subject in teacher_subject:
                    if subject not in selected_subjects:
                        subject.delete()
                for subject in selected_subjects:
                    if subject not in teacher_subject:
                        Subject.objects.create(name=subject.name, teacher=user, klass=subject.klass).save()
            else: #student admin
                selected_classes = extra_form.cleaned_data['classes']
                for klass in Klass.objects.all():
                    if klass in selected_classes:
                        if not Klass.objects.filter(class_name=klass.class_name, student=user).exists():
                            klass.student.add(user)
                    else:
                        klass.student.remove(user)
            return redirect('show_users')
        forms = [form, extra_form]
        return render(request, 'form.html', {'form': forms, 'multiple' : True})


#TODO fix for current models
class AssignSubject(View):
    def get(self, request):
        form = AddSubjectForm()
        return render(request, 'form.html', {'form': form})

    def post(self, request):
        form = AddSubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home',)
        return render(request, 'form.html', {'form': form})

class CreateClass(View):
    def get(self, request):
        form = CreateClassForm()
        students = User.objects.filter(groups__name='Students')
        #TODO zrob templatke, gdzie bedzie lista uzytkownikow, podobne jak przy wystawianiu ocen
        return render(request, 'create_class.html', {'form': form, 'students': students})

    def post(self, request):
        form = CreateClassForm(request.POST)
        students = User.objects.filter(groups__name='Students')
        if form.is_valid():
            new_class = Klass.objects.create(class_name=form.cleaned_data['class_name'])
            for student in students:
                belongs = request.POST.get(f'{student.id}')
                if belongs:
                    new_class.student.add(student)
            new_class.save()
            return redirect('home')
        return render(request, 'create_class.html', {'form': form, 'students': students})

