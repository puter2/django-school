from django.contrib import admin

from accounts.models import Role
from school.models import Student, Teacher, Grade, Subject

# Register your models here.
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Grade)
admin.site.register(Role)
admin.site.register(Subject)
