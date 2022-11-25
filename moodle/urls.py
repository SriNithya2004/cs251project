from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
#from views import *

urlpatterns = [
  path('', auth_views.LoginView.as_view(), name='login'),
  path('logout/', auth_views.LogoutView.as_view(), name='logout'),
  path('homepage/', views.homepage, name='homepage'),
  path('signup/', views.user_register, name='signup'),
  path('profile/',views.profile,name = 'profile'),
  path('profile_change/',views.profile_change,name = 'profile_change'),
  path('password/',views.change_pass,name = 'change_pass'),
]