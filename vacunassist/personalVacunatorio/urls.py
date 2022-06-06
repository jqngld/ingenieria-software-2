from django.urls import path
from personalVacunatorio.views import *


urlpatterns = [
    path('', home_personal, name='home_personal'),
    path('inicio_sesion/', login_personal, name='login_personal'),
    path('turnos/', listar_turnos, name='listar_turnos'),
]
