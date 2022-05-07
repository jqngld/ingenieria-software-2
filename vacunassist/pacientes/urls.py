from django.urls import path
from pacientes.views import *


urlpatterns = [
    path('', home),
    path('login/', login, name='login'),
    path('signup/credentials/', register_credentials, name='register_credentials')
]