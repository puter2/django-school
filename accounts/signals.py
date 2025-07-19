from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Role
from school.models import Student, Teacher



@receiver(post_save, sender=Role)
def create_or_update_user_role_form(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'student':
            Student.objects.create(user=instance.user)
        elif instance.role == 'teacher':
            Teacher.objects.create(user=instance.user)
