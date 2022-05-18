from django.urls import path
from pacientes.views import *
from django.contrib.auth.views import LoginView
urlpatterns = [
    path('', home, name='home'),
    path('login/', login, name='login'),
    path('signup/', signup, name='signup'),
    path('login_error/', login_error, name='login_error'),
    path('inicio_pacientes/', inicio_pacientes, name='inicio_pacientes'),
]