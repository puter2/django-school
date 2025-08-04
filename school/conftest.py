import pytest
from django.contrib.auth.models import User


from school.models import Grade, Subject


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

