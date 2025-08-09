from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views import View

from school.conftest import subjects
from school.forms import GradesForm, AddSubjectForm, AddSubjectToTeacherForm, AddGradeObjectForm
from school.models import Grade, Subject, GradeObject


#TODO credential check

# Create your views here.
#TODO add easy editing, add average, implement search
class GradesView(View):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            # print(user.groups.all())
            if user.groups.all()[0].name == 'Students':
                subjects = Subject.objects.all()
                grade_subject = []
                # subject : grades
                for subject in subjects:
                    grades = Grade.objects.filter(student=user, topic__subject=subject)
                    grade_subject.append({
                        'subject': subject,
                        'grades': grades
                    })
                return render(request, 'show_grades_student.html', {'grade_subject': grade_subject})
            if user.groups.all()[0].name == 'Teachers':
                filter_subject = request.GET.get('subject')
                topics = GradeObject.objects.all()
                if filter_subject:
                    topics = topics.filter(subject=filter_subject)
                students = User.objects.filter(groups__name='Students')
                grades_data = []
                for student in students:
                    student_grades = Grade.objects.filter(student=student).select_related('topic')
                    topic_grades = []
                    for topic in topics:
                        grade = None
                        for g in student_grades:
                            if g.topic_id == topic.id:
                                grade = g
                                break
                        topic_grades.append(grade)
                    grades_data.append({
                        'student': student,
                        'grades': topic_grades,
                    })
                return render(request, 'show_grades_teacher.html', {'grades_data': grades_data, 'topics': topics, 'students': students})
        return redirect('home')

#TODO remove
class AddGradeView(View):

    def get(self, request):
        form = GradesForm()
        return render(request,'form.html', {'form': form})
    #
    # def post(self, request):
    #     teacher = Teacher.objects.get(user=request.user)
    #     print(teacher)
    #     form = GradesForm(request.POST, teacher=teacher)
    #     if form.is_valid():
    #         print('a')
    #         grade = form.cleaned_data['grade']
    #         student = form.cleaned_data['student']
    #         subject = form.cleaned_data['subject']
    #         new_grade = Grade.objects.create(grade=grade, student=student, teacher=teacher, subject=subject)
    #         new_grade.save()
    #         return redirect('home',)
    #     print('nie poszloi')
    #     return render(request, 'form.html', {'form': form})

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
        group = request.GET.get('group')
        if name:
            users = users.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name))
        if group:
            #TODO make selecting group more dynamic
            users = users.filter(groups__name__contains=group)
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


class CreateGradeObjectView(View):
    def get(self, request):
        user = request.user
        form = AddGradeObjectForm(user=user)
        return render(request, 'form.html', {'form': form})

    def post(self, request):
        user = request.user
        form = AddGradeObjectForm(request.POST, user=user)
        if form.is_valid():
            form.save()
            return redirect('home')
        return render(request, 'form.html', {'form': form})

class AddGradesView(View):
    def get(self, request):
        students = User.objects.filter(groups__name__contains='student')
        user = request.user
        grade_obj = GradeObject.objects.filter(subject__teacher=user)
        return render(request, 'add_grades.html',
                      {
                          'students': students,
                          'grade_obj': grade_obj,
                          'selected_grade_obj': True
                      }
                      )

    def post(self, request):
        students = User.objects.filter(groups__name__contains='student')
        user = request.user
        grade_obj_name = request.POST.get('grade_obj')
        grade_obj = GradeObject.objects.get(name=grade_obj_name)
        for student in students:
            grade_val = request.POST.get(str(student.id))
            print(student.id, grade_val)
            if grade_val:
                print('a')
                new_grade = Grade.objects.create(student=student,
                                                 grade=grade_val,
                                                 teacher=user,
                                                 topic=grade_obj)
                new_grade.save()
        return redirect('home')

