from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    is_customer = models.BooleanField('customer status', default=False)
    is_seller = models.BooleanField('seller status', default=False)

COLOR_CHOICES = (
    ('carpenter','CARPENTER'),
    ('plumber', 'PLUMBER'),
    ('electrician','ELECTRICIAN'),
    ('mechanic','MECHANIC'),
    ('painter','PAINTER'),
)

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    desc = models.CharField(max_length=200,default='na')
    locations = models.CharField(max_length=100,default='kolkata')
    pin = models.IntegerField(default=1)
    job = models.CharField(max_length=100, choices=COLOR_CHOICES, default='carpenter')
    rate = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

class CustomerAppointments(models.Model):
    customer = models.OneToOneField(User,on_delete=models.CASCADE)
    appnts = models.ManyToManyField(User,related_name='+')
     
    def __str__(self):
        return self.customer.username
  