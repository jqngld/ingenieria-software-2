from django.urls import path
from personalVacunatorio.views import *


urlpatterns = [
    path('', home_personal, name='home_personal'),
    path('turnos/', listar_turnos, name='listar_turnos'),
    path('inicio_sesion/', login_personal, name='login_personal'),
    path('cerrar_sesion/', logout_personal, name='logout_personal'),
    path('login_error/', login_error_personal, name='login_error_personal'),
]
