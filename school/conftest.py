import pytest
from django.contrib.auth.models import User

from accounts.models import Role


@pytest.fixture
def admin():
    return User.objects.create_superuser(username='admin', password='<PASSWORD>')

@pytest.fixture
def users():
    lst = []
    lst.append(User.objects.create_user(username='user1', password='<PASSWORD>'))
    lst.append(User.objects.create_user(username='user2', password='<PASSWORD>'))
    lst.append(User.objects.create_user(username='user3', password='<PASSWORD>'))
    return lst

@pytest.fixture
def students(users):
    lst = []
    lst.append(Role.objects.create(user=users[0], role='Student'))
    lst.append(Role.objects.create(user=users[1], role='Student'))
    lst.append(Role.objects.create(user=users[2], role='Student'))
    return lst

@pytest.fixture
def teachers(users):
    lst = []
    lst.append(Role.objects.create(user=users[0], role='Teacher'))
    lst.append(Role.objects.create(user=users[1], role='Teacher'))
    lst.append(Role.objects.create(user=users[2], role='Teacher'))
    return lst