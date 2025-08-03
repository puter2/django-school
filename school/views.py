from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views import View

from school.forms import GradesForm, AddSubjectForm, AddSubjectToTeacherForm
from school.models import Grade, Student, Teacher

#TODO credential check

# Create your views here.
class GradesView(View):
#TODO refactor
    def get(self, request):
        user = request.user
        name = request.GET.get('name')
        if user.role.role == 'teacher':
            teacher = Teacher.objects.get(user=user)
            grades = Grade.objects.filter(teacher=teacher)
            grades = grades.filter(Q(student__user__first_name__contains=name) | Q(student__user__last_name__contains=name)) if name else grades
            return render(request, 'show_grades.html', {'grades': grades})
        elif user.role.role == 'student':
            student = Student.objects.get(user=user)
            grades = Grade.objects.filter(student=student)
            grades = grades.filter(Q(teacher__user__first_name__contains=name) | Q(
                teacher__user__last_name__contains=name)) if name else grades
            return render(request, 'show_grades.html', {'grades': grades})
        return redirect('home')

#TODO check if grade is valid
class AddGradeView(View):

    def get(self, request):
        teacher = Teacher.objects.get(user=request.user)
        form = GradesForm(teacher=teacher)
        return render(request,'form.html', {'form': form})

    def post(self, request):
        teacher = Teacher.objects.get(user=request.user)
        print(teacher)
        form = GradesForm(request.POST, teacher=teacher)
        if form.is_valid():
            print('a')
            grade = form.cleaned_data['grade']
            student = form.cleaned_data['student']
            subject = form.cleaned_data['subject']
            new_grade = Grade.objects.create(grade=grade, student=student, teacher=teacher, subject=subject)
            new_grade.save()
            return redirect('home',)
        print('nie poszloi')
        return render(request, 'form.html', {'form': form})

#TODO testy

class AddSubjectView(View):

    def get(self, request):
        form = AddSubjectForm()
        return render(request, 'form.html', {'form': form})

    def post(self, request):
        form = AddSubjectForm(request.POST)
        if form.is_valid():
            subject = form.save()
            return redirect('home',)
        return render(request, 'form.html', {'form': form})

class ShowUsersView(View):
    #TODO change view so that it's consistent
    def get(self, request):
        users = User.objects.all()
        name = request.GET.get('name')
        role = request.GET.get('role')
        if name:
            users = users.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name))
        if role:
            users = users.filter(role__role=role)
        return render(request, 'show_users.html', {'users': users})


class DeleteGradeView(View):
    def get(self, request, pk):
        grade = Grade.objects.get(pk=pk)
        return render(request, 'delete_form.html', {'obj_name': grade})

    def post(self, request, pk):
        if request.POST.get('operation') == 'Yes':
            grade = Grade.objects.get(pk=pk)
            grade.delete()
        return redirect('grades')

class EditGradeView(View):
    def get(self, request, pk):
        grade = Grade.objects.get(pk=pk)
        form = GradesForm(instance=grade)
        return render(request, 'form.html', {'form': form})

    def post(self, request, pk):
        grade = Grade.objects.get(pk=pk)
        form = GradesForm(request.POST, instance=grade)
        if form.is_valid():
            form.save()
            return redirect('grades')
        return render(request, 'form.html', {'form': form})

    #TODO assign subject view
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