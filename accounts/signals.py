from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
# from .models import Role
# from school.models import Student, Teacher


# @receiver(post_save, sender=Role)
# def create_or_update_user_role_form(sender, instance, created, **kwargs):
#     if created:
#         if instance.role == 'student':
#             Student.objects.create(user=instance.user)
#         elif instance.role == 'teacher':
#             Teacher.objects.create(user=instance.user)

@receiver(post_migrate)
def create_groups(sender, **kwargs):
    Group.objects.get_or_create(name='Admins')
    Group.objects.get_or_create(name='Teachers')
    Group.objects.get_or_create(name='Students')
