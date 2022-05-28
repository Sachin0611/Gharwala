from django.db.models.signals import post_save

from .models import Profile, User
from django.dispatch import receiver

@receiver(post_save, sender=User, dispatch_uid='save_new_user_profile')
def save_profile(sender, instance, created, **kwargs):
    user = instance
    if created:
        profile = Profile(user=User)
        profile.save()

