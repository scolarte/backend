from django.db import models
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    is_client = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)


### User Profile ###

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthdate = models.DateField(null=True, blank=True)
    dni = models.CharField(max_length=30, blank=True)
    phone_number = models.CharField(max_length=30, blank=True)
    shipping_address = models.CharField(max_length=100, blank=False)
    reference = models.CharField(max_length=100, blank=False)
    shipping_department = models.CharField(max_length=100, blank=False)
    shipping_province = models.CharField(max_length=100, blank=False)
    shipping_district = models.CharField(max_length=100, blank=False)
    photo = models.ImageField(upload_to='profile_pics', default='profile_pics/default_profile_pic_white.png')

    def __str__(self):
        return str(self.user.first_name) + "'s profile"



@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
