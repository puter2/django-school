from django.contrib.auth.models import User
from django.test import TestCase
import pytest
from django.test import Client
from django.urls import reverse

from accounts.models import Role
from school.models import Student, Teacher


# Create your tests here.

def test_home_view():
    c = Client()
    response = c.get('/')
    assert response.status_code == 200

@pytest.mark.django_db
def test_creating_students_while_creating_roles(students):
    assert len(students) == len(Role.objects.filter(role='Student'))

@pytest.mark.django_db
def test_creating_teachers_while_creating_roles(teachers):
    assert len(teachers) == len(Role.objects.filter(role='Teacher'))

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