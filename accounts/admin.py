from django.contrib import admin

from school.models import Grade, Subject, Grade_object, Klass

# Register your models here.
admin.site.register(Grade)
admin.site.register(Subject)
admin.site.register(Grade_object)
admin.site.register(Klass)