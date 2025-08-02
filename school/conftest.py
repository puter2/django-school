import pytest
from django.contrib.auth.models import User

from accounts.models import Role
from school.models import Grade, Subject, Teacher


@pytest.fixture
def admin():
    return User.objects.create_superuser(username='admin', password='<PASSWORD>')

@pytest.fixture
def subjects():
    lst = []
    lst.append(Subject.objects.create(subject='Subject 1'))
    lst.append(Subject.objects.create(subject='Subject 2'))
    lst.append(Subject.objects.create(subject='Subject 3'))
    return lst

@pytest.fixture
def users():
    lst = []
    lst.append(User.objects.create_user(username='user1', password='<PASSWORD>', first_name='user1', last_name='student'))
    lst.append(User.objects.create_user(username='user2', password='<PASSWORD>', first_name='user2', last_name='student'))
    lst.append(User.objects.create_user(username='user3', password='<PASSWORD>', first_name='user3', last_name='student'))
    lst.append(User.objects.create_user(username='user4', password='<PASSWORD>', first_name='user4', last_name='teacher'))
    lst.append(User.objects.create_user(username='user5', password='<PASSWORD>', first_name='user5', last_name='teacher'))
    lst.append(User.objects.create_user(username='user6', password='<PASSWORD>', first_name='user6', last_name='teacher'))
    return lst

@pytest.fixture
def students_role(users):
    lst = []
    lst.append(Role.objects.create(user=users[0], role='student'))
    lst.append(Role.objects.create(user=users[1], role='student'))
    lst.append(Role.objects.create(user=users[2], role='student'))
    return lst

@pytest.fixture
def teachers_role(users):
    lst = []
    lst.append(Role.objects.create(user=users[-1], role='teacher'))
    lst.append(Role.objects.create(user=users[-2], role='teacher'))
    lst.append(Role.objects.create(user=users[-3], role='teacher'))
    return lst

@pytest.fixture
def teachers_subjects(teachers_role, subjects):
    teachers = Teacher.objects.all()
    for teacher, subject in zip(teachers, subjects):
        teacher.subject.add(subject)
        print(teacher.subject.all())
    return teachers