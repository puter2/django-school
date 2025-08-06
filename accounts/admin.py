from django.contrib import admin

from school.models import Grade, Subject, GradeObject, Klass

# Register your models here.
admin.site.register(Grade)
admin.site.register(Subject)
admin.site.register(GradeObject)
admin.site.register(Klass)