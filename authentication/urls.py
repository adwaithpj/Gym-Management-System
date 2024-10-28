from django.urls import path,include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'authentication'

urlpatterns = [
    path('',views.test,name='test'),
    path('login/',views.login_page,name='login'),
    path('signup/',views.signup,name='signup'),
    path('logout/',views.logout_page,name='logout'),
    path('complete_signup/',views.complete_signup,name='complete_signup'),
    path('password_reset/',views.password_reset,name='password_reset'),
]   