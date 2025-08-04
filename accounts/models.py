from django.contrib.auth.models import User
from django.db import models

# Create your models here.

# old model
# class Role(models.Model):
#     ROLE_CHOICES = (
#         ('admin', 'Admin'),
#         ('student', 'Student'),
#         ('teacher', 'Teacher'),
#     )
#
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     role = models.CharField(max_length=10, choices=ROLE_CHOICES)
#
#     def __str__(self):
#         return self.role
