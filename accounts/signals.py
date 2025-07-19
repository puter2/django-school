# accounts/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Role

#bit of extra code so that role is created alongside new user

@receiver(post_save, sender=User)
def create_user_role(sender, instance, created, **kwargs):
    if created:
        Role.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_role(sender, instance, **kwargs):
    instance.role.save()