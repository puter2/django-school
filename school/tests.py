from django.contrib.auth.models import User
from django.test import TestCase
import pytest
from django.test import Client
from django.urls import reverse

from accounts.models import Role
from school.models import Student, Teacher, Grade


# Create your tests here.

def test_home_view():
    c = Client()
    response = c.get('/')
    assert response.status_code == 200

@pytest.mark.django_db
def test_creating_students_while_creating_roles(students_role):
    assert len(students_role) == len(Student.objects.all())

@pytest.mark.django_db
def test_creating_teachers_while_creating_roles(teachers_role):
    assert len(teachers_role) == len(Teacher.objects.all())

@pytest.mark.django_db
@pytest.mark.parametrize('username,password',[
    ('stud1','<PASSWORD>'),
    ('stud2','<PASSWORD>'),
])
def test_registering_students_view_post(username, password):
    c = Client()
    url = reverse('register')
    response = c.post(url, {
        'username': username,
        'password1': password,
        'password2': password,
        'role': 'student',
    })
    assert response.status_code == 302
    assert User.objects.filter(username=username).exists()
    user = User.objects.get(username=username)
    assert Student.objects.filter(user=user).exists()

@pytest.mark.django_db
@pytest.mark.parametrize('username,password',[
    ('t1','<PASSWORD>'),
    ('t2','<PASSWORD>'),
])
def test_registering_teacher_view_post(username, password):
    c = Client()
    url = reverse('register')
    response = c.post(url, {
        'username': username,
        'password1': password,
        'password2': password,
        'role': 'teacher',
    })
    assert response.status_code == 302
    assert User.objects.filter(username=username).exists()
    user = User.objects.get(username=username)
    assert Teacher.objects.filter(user=user).exists()

@pytest.mark.django_db
def test_adding_grades_view_post(students_role, teachers_subjects):
    teachers = Teacher.objects.all()
    students = Student.objects.all()
    for student, teacher in zip(students, teachers):
        student_user = student.user
        teacher_user = teacher.user
        c = Client()
        c.force_login(teacher_user)
        url = reverse('add_grade')
        response = c.post(url, {
            'grade': 1.,
            'student': student_user.id,
            'subject': teacher.subject.all()[0].id,
        })
        assert response.status_code == 302
        assert Grade.objects.filter(student=student_user.id).exists()

#TODO testuj kazdy widok