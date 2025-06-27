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

