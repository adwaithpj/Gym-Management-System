from django.urls import path,include

from members.views import GymMembersAPI

app_name = 'api'


urlpatterns = [
    path('members/',GymMembersAPI.as_view(),name='api_members'),
    path('members/<int:id>/', GymMembersAPI.as_view(), name='member-detail'),
]