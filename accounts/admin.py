from django.contrib import admin

from school.models import Grade, GradeObject, Klass, Subject

# Register your models here.
admin.site.register(Grade)
admin.site.register(Subject)
admin.site.register(GradeObject)
admin.site.register(Klass)
