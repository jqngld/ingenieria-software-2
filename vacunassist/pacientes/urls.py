from django.urls import path
from pacientes.views import *


urlpatterns = [
    path('', home),
    path('login/', login),
]