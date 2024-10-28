from django.contrib import admin
from .models import GymAdmin
from django.contrib.auth.admin import UserAdmin


admin.site.register(GymAdmin,UserAdmin)