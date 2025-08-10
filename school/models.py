from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User
from django.db.models import ManyToManyField


# Create your models here.

class Klass(models.Model):
    student = ManyToManyField(User)
    class_name = models.CharField(max_length=100, db_column='class', verbose_name='Class', null=True, unique=True)
    def __str__(self):
        return f'{self.class_name}'

class Subject(models.Model):
    subject = models.CharField(max_length=100, unique=True, verbose_name='Subject')
    teacher = models.ManyToManyField(User, null=True, verbose_name='Teacher')
    def __str__(self):
        return self.subject

class GradeObject(models.Model):
    name = models.CharField(max_length=100)
    weight = models.FloatField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.name

class Grade(models.Model):
    grade = models.FloatField()
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_grades')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teacher_grades')
    topic = models.ForeignKey(GradeObject, on_delete=models.CASCADE, null=True)
    description = models.TextField(null=True, blank=True)
    def __str__(self):
        return f'{self.grade} {self.topic} {self.teacher}'

