from django.db import models
from authentication.models import GymAdmin as User
from django.core.validators import MinLengthValidator

# Create your models here.

class Subscription(models.Model):
    subs = models.CharField(max_length=255)
    
    class Meta:
        ordering = ('subs',)
        verbose_name_plural = 'Subscriptions'
    
    def __str__(self):
        return self.subs

class Paymentmethod(models.Model):
    method = models.CharField(max_length=255)
    
    class Meta:
        ordering = ('method',)
    
    def __str__(self) :
        return self.method

class GymMembers(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=200,null=True, blank=True)
    phone_number = models.CharField(max_length=10)
    address = models.CharField(max_length=500)
    city = models.CharField(max_length=100)
    sub_type = models.ForeignKey(Subscription,related_name='gym_memberships',on_delete=models.CASCADE)
    created_by = models.ForeignKey(User,related_name='gym_memberships',on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    pay_method = models.ForeignKey(Paymentmethod,related_name='gym_memberships',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    renew_date = models.DateTimeField(null=True, blank=True)
    expiry_date = models.DateTimeField(null=True, blank=True)
    # user_profile_image = models.ImageField(upload_to='members', blank=True, null=True)
    user_profile_image = models.CharField(max_length=500, blank=True, null=True)
    
    
    class Meta:
        ordering = ('name',)
    
    def __str__(self):
        return self.name