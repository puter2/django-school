import pytest
from django.contrib.auth.models import User

from accounts.models import Role
from school.models import Grade


@pytest.fixture
def admin():
    return User.objects.create_superuser(username='admin', password='<PASSWORD>')

@pytest.fixture
def users():
    lst = []
    lst.append(User.objects.create_user(username='user1', password='<PASSWORD>', first_name='user1', last_name='student'))
    lst.append(User.objects.create_user(username='user2', password='<PASSWORD>', first_name='user2', last_name='student'))
    lst.append(User.objects.create_user(username='user3', password='<PASSWORD>', first_name='user3', last_name='student'))
    lst.append(User.objects.create_user(username='user4', password='<PASSWORD>'))
    lst.append(User.objects.create_user(username='user5', password='<PASSWORD>'))
    lst.append(User.objects.create_user(username='user6', password='<PASSWORD>'))
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

# @pytest.fixture
# def grades(students, teachers):
#     lst = []
#     lst.append(Grade.objects.create(grade=1, student=students[0], teacher=teachers[0]))
#     lst.append(Grade.objects.create(grade=2, student=students[1], teacher=teachers[1]))
#     lst.append(Grade.objects.create(grade=3, student=students[2], teacher=teachers[2]))
#     return lst