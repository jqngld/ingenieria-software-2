from django.urls import path
from pacientes.views import *


urlpatterns = [
    path('', home),
    path('login/', login, name='login'),
    path('signup/', signup, name='signup'),
    path('mail/', mail, name='mail')
]