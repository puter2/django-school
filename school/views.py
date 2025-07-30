from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views import View

from school.forms import GradesForm, AddSubjectForm
from school.models import Grade, Student, Teacher


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
            grade = form.cleaned_data['grade']
            student = form.cleaned_data['student']
            subject = form.cleaned_data['subject']
            new_grade = Grade.objects.create(grade=grade, student=student, teacher=teacher, subject=subject)
            new_grade.save()
            return redirect('home',)
        return render(request, 'form.html', {'form': form})

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
        name = request.POST['name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        role = request.POST['role']
        subject = request.POST['subject']
        user = User.objects.get(username=username)
        if role == 'student':
            new_student = Student.objects.create(user=user, name=name, lastname=last_name)
            new_student.save()
        else:
            new_teacher = Teacher.objects.create(user=user, name=name, lastname=last_name, subject=subject)
            new_teacher.save()
        return redirect('home',)

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