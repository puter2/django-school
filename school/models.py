from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)

    def __str__(self):
        return self.name + ' ' + self.lastname

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    def __str__(self):
        return self.name + ' ' + self.lastname

class Grade(models.Model):
    grade = models.FloatField()
    subject = models.CharField(max_length=100)
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    teacher = models.OneToOneField(Teacher, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.grade) + self.subject + str(self.teacher)