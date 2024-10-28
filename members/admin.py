from django.contrib import admin

from .models import Subscription,GymMembers,Paymentmethod

# Register your models here.

admin.site.register(Subscription)
admin.site.register(Paymentmethod)
admin.site.register(GymMembers)