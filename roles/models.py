from django.db import models
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
import random


class User(AbstractUser):
    is_client = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)
    


### Profile ####

# Helper Functions
def random_digits():
    return "%0.12d" % random.randint(0, 999999999999)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthdate = models.DateField(null=True, blank=True)
    cedula_ruc = models.CharField(max_length=30, blank=True)
    telephone = models.CharField(max_length=30, blank=True)
    mobile = models.CharField(max_length=30, blank=True)
    address = models.CharField(max_length=100, blank=False)
    address_reference = models.CharField(max_length=100, blank=False)
    location = models.CharField(max_length=100, blank=True, null=True)
    shipping_address = models.CharField(max_length=100, blank=False)    
    photo = models.ImageField(upload_to='profile_pics', default='profile_pics/default_profile_pic.png')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user.username) + "'s profile"



@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
