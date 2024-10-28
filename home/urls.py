from django.urls import path,include

from . import views

app_name = 'home'

urlpatterns = [
    path('home/',views.home,name='dashboard'),
    path('',views.update_status,name='update'),
    path('refresh/',views.update_status_members,name='refresh')
    
]
