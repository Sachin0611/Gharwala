from django.db.models.signals import post_save
from .models import Profile, User,CustomerAppointments
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        CustomerAppointments.objects.create(customer= instance)
        



@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    instance.customerappointments.save()

