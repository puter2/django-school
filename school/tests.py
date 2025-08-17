
from django.contrib.auth.models import User, Group
from django.test import TestCase
import pytest
from django.test import Client
from django.urls import reverse

from school.models import Grade, Klass, Subject, GradeObject


# Create your tests here.

def test_home_view():
    c = Client()
    response = c.get('/')
    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrize('username,password',[
    ('stud1','<PASSWORD>'),
    ('stud2','<PASSWORD>'),
])
def test_registering_students_view_post(username, password):
    c = Client()
    url = reverse('register')
    group=Group.objects.get(name='Students')
    response = c.post(url, {
        'username': username,
        'password1': password,
        'password2': password,
        'group': group.id,
    })
    assert response.status_code == 302
    assert User.objects.filter(username=username).exists()

@pytest.mark.django_db
@pytest.mark.parametrize('username,password',[
    ('t1','<PASSWORD>'),
    ('t2','<PASSWORD>'),
])
def test_registering_teacher_view_post(username, password):
    c = Client()
    url = reverse('register')
    group = Group.objects.get(name='Teachers')
    response = c.post(url, {
        'username': username,
        'password1': password,
        'password2': password,
        'group': group.id,
    })
    assert response.status_code == 302
    assert User.objects.filter(username=username).exists()

@pytest.mark.django_db
def test_deleting_users_view_post(users):
    c = Client()
    for user in users:
        u_id = user.id
        url = reverse(f'delete_user', args=[u_id])
        response = c.post(url, {'operation':'Yes'})
        assert response.status_code == 302
        assert not User.objects.filter(id=u_id).exists()

# TODO
# @pytest.mark.django_db
# def test_editing_users_view_post(users):
#     c = Client()
#     for user in users:
#         u_id = user.id
#         url = reverse(f'edit_user', args=[u_id])
#         response = c.post(url, {'username':'edited'})
#         assert response.status_code == 302

@pytest.mark.django_db
def test_add_class_view_post(users):
    c = Client()
    url = reverse('add_class')
    students = User.objects.filter(groups__name='Students')
    url = reverse('add_class')
    students_in_class = {f'{student.id}': True for student in students}
    print(students_in_class)
    context = {'class_name': 'test',}
    context.update(students_in_class)
    response = c.post(url, context)
    assert response.status_code == 302
    assert Klass.objects.filter(class_name='test').exists()
    assert Klass.objects.filter(class_name='test')[0].student.all().count() == students.count()

@pytest.mark.django_db
@pytest.mark.parametrize('teacher_id,klass_id,name',[
    (4,1,'test1'),
    (5,2,'test2'),
    (6,2,'test3'),
])
def test_add_subject_view_post(users, klasses, teacher_id, name, klass_id):
    c = Client()
    teacher = User.objects.get(id=teacher_id)
    klass = Klass.objects.get(id=klass_id)
    url = reverse('add_subject')
    response = c.post(url, {'klass': klass.id, 'teacher': teacher.id, 'name':name})
    assert response.status_code == 302
    assert Subject.objects.filter(name=name).exists()

@pytest.mark.django_db
def test_create_grade_object_view_post(subjects):
    c = Client()
    teacher = User.objects.filter(groups__name='Teachers')[0]
    c.force_login(teacher)
    subject = Subject.objects.filter(teacher=teacher)[0]
    url = reverse('create_grade_object')
    response = c.post(url, {'name':'test1', 'subject':subject.id, 'weight':2})
    assert response.status_code == 302
    assert GradeObject.objects.filter(subject=subject).exists()


@pytest.mark.django_db
def test_add_grades_view_post(grade_objects, users):
    c = Client()
    c.force_login(users[3])
    url = reverse('add_grades')
    # url = reverse('add_grades')
    response = c.post(f'{url}?grade_obj={grade_objects[0].name}',{'1':1.})
    assert response.status_code == 302
    assert Grade.objects.filter(topic=grade_objects[0]).exists()


@pytest.mark.django_db
def test_editing_users_view_post(users):
    c = Client()
    url = reverse('edit_user', args=[users[0].id])
    response = c.post(f'{url}', {'first_name':'edited',
                                 'last_name':'edited',
                                 'groups':Group.objects.get(name='Students').id,
                                 })
    assert response.status_code == 302
    assert User.objects.filter(username=users[0]).exists()
    assert User.objects.filter(username=users[0])[0].first_name == 'edited'

# @pytest.mark.django_db
# def test_adding_grades_view_post(students_role, teachers_subjects):
#     # teachers = Teacher.objects.all()
#     # students = Student.objects.all()
#     # for student, teacher in zip(students, teachers):
#     #     student_user = student.user
#     #     teacher_user = teacher.user
#     #     c = Client()
#     #     c.force_login(teacher_user)
#     #     url = reverse('add_grade')
#     #     response = c.post(url, {
#     #         'grade': 1.,
#     #         'student': student_user.id,
#     #         'subject': teacher.subject.all()[0].id,
#     #     })
#     #     assert response.status_code == 302
#     #     assert Grade.objects.filter(student=student_user.id).exists()

#TODO testuj kazdy widok