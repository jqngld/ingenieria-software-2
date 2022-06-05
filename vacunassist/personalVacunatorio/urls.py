from django.urls import path
from personalVacunatorio.views import *


urlpatterns = [
    path('', home, name='home'),
    path('inicio_sesion/', login, name='login'),
    path('turnos/', listar_turnos, name='listar_turnos'),
]
