from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View

from school.forms import GradesForm
from school.models import Grade, Student, Teacher


# Create your views here.
class GradesView(View):

    def get(self, request):
        grades = Grade.objects.all()
        return render(request, 'show_grades.html', {'grades': grades})

class AddGradeView(View):

    def get(self, request):
        # teachers = Teacher.objects.get(user=request.user)
        # print(teachers)
        form = GradesForm()
        return render(request,'form.html', {'form': form})

    def post(self, request):
        form = GradesForm(request.POST)
        if form.is_valid():
            grade = form.cleaned_data['grade']
            student = form.cleaned_data['student']
            # VERY TEMPORARY
            teacher = Teacher.objects.get(user=request.user)
            subject = Teacher.objects.get(user=request.user).subject
            ###############
            print(request.user)
            new_grade = Grade.objects.create(grade=grade, student=student, teacher=teacher, subject=subject)
            new_grade.save()
            return redirect('home',)
        return render(request, 'form.html', {'form': form})

#TODO widok admina gdzie admin widzi nowych userow i przyporzadkuje ich do nauczyciela/ucznia

class AssignUserRoleView(View):
    def get(self, request):
        users = User.objects.values_list('id', flat=True)
        students = Student.objects.values_list('user', flat=True)
        teachers = Teacher.objects.values_list('user', flat=True)
        processed = students.union(teachers)
        print(users.difference(processed))
        print(users, students, teachers)
        unassigned = User.objects.filter(id__in=users.difference(processed))
        print(unassigned)
        for user in unassigned:
            print(user)
        return  render(request, 'AssignUserRoleForm.html', {'unassigned': unassigned})

    def post(self, request):
        print(request.POST)
        name = request.POST['name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        role = request.POST['role']
        subject = request.POST['subject']
        user = User.objects.get(username=username)
        print(user)
        if role == 'student':
            new_student = Student.objects.create(user=user, name=name, lastname=last_name)
            new_student.save()
        else:
            new_teacher = Teacher.objects.create(user=user, name=name, lastname=last_name, subject=subject)
            new_teacher.save()
        return redirect('home',)