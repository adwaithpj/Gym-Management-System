from django.urls import path 
from . import views

app_name = 'members'

urlpatterns = [
    path('add_member/',views.add_member,name='add'),
    path('view_members/',views.view_members,name='view'),
    path('profile/<int:pk>/',views.member_profile,name='profile'),

]