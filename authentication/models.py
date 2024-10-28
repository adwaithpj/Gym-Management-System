from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from .manager import UserManager 

class GymAdmin(AbstractUser):
    
    username = models.CharField(unique=True,null=True,blank=True,max_length=255)
    phone_number = models.IntegerField(unique=True,blank=True,null=True)
    email = models.EmailField(unique=True)
    dob = models.DateField(blank=True,null=True)
    user_profile_image = models.ImageField(upload_to='profile', blank=True, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']