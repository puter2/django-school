from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    class_name = models.CharField(max_length=100, db_column='class', verbose_name='Class', null=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

class Subject(models.Model):
    subject = models.CharField(max_length=100)
    def __str__(self):
        return self.subject

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subject = models.ManyToManyField(Subject, verbose_name='Subject')
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

class Grade(models.Model):
    grade = models.FloatField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.grade} {self.subject} {self.teacher}'

