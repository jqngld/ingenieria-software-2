from django.urls import path
from pacientes.views import *
from django.contrib.auth.views import LoginView
urlpatterns = [
    path('', home),
    path('login/', login, name='login'),
    path('signup/', signup, name='signup'),
    path('mail/', mail, name='mail')
]