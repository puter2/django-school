import pytest
from django.contrib.auth.models import User, Group

from school.models import Subject, Klass, GradeObject


@pytest.fixture
def admin():
    return User.objects.create_superuser(username='admin', password='<PASSWORD>')


@pytest.fixture
def users():
    lst = []
    u = User.objects.create_user(username='user1', password='<PASSWORD>', first_name='user1', last_name='student')
    u.groups.add(Group.objects.get_or_create(name='Students')[0])
    lst.append(u)
    u = User.objects.create_user(username='user2', password='<PASSWORD>', first_name='user2', last_name='student')
    u.groups.add(Group.objects.get_or_create(name='Students')[0])
    lst.append(u)
    u = User.objects.create_user(username='user3', password='<PASSWORD>', first_name='user3', last_name='student')
    u.groups.add(Group.objects.get_or_create(name='Students')[0])
    lst.append(u)
    u = User.objects.create_user(username='user4', password='<PASSWORD>', first_name='user4', last_name='student')
    u.groups.add(Group.objects.get_or_create(name='Teachers')[0])
    lst.append(u)
    u = User.objects.create_user(username='user5', password='<PASSWORD>', first_name='user5', last_name='student')
    u.groups.add(Group.objects.get_or_create(name='Teachers')[0])
    lst.append(u)
    u = User.objects.create_user(username='user6', password='<PASSWORD>', first_name='user6', last_name='student')
    u.groups.add(Group.objects.get_or_create(name='Teachers')[0])
    lst.append(u)
    return lst

@pytest.fixture
def klasses():
    lst = []
    lst.append(Klass.objects.create(class_name='test'))
    lst.append(Klass.objects.create(class_name='test2'))
    return lst

@pytest.fixture
def subjects(klasses, users):
    lst = []
    lst.append(Subject.objects.create(name='Subject1', klass=klasses[0], teacher=users[3]))
    lst.append(Subject.objects.create(name='Subject2', klass=klasses[1], teacher=users[4]))
    lst.append(Subject.objects.create(name='Subject3', klass=klasses[1], teacher=users[5]))
    return lst

@pytest.fixture
def grade_objects(subjects):
    lst = []
    lst.append(GradeObject.objects.create(subject=subjects[0], weight=0, name='test1'))
    lst.append(GradeObject.objects.create(subject=subjects[1], weight=1, name='test2'))
    lst.append(GradeObject.objects.create(subject=subjects[2], weight=2, name='test3'))
    return lst