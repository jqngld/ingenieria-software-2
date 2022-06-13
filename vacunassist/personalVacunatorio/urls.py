from django.urls import path
from personalVacunatorio.views import *


urlpatterns = [
    path('', home_personal, name='home_personal'),
    path('turnos/', listar_turnos_diarios, name='listar_turnos_diarios'),
    path('inicio_sesion/', login_personal, name='login_personal'),
    path('cerrar_sesion/', logout_personal, name='logout_personal'),
    path('login_error/', login_error_personal, name='login_error_personal'),
    path('devolucion/<int:vacuna_aplicada>/', devolucion, name='devolucion'),
    path('turnos/vacunacion_exitosa/<int:turno_id>/<int:paciente_dni>/<str:vacuna_nombre>/', vacunacion_exitosa, name="vacunacion_exitosa"),
    path('turnos/vacunacion_fallida/<int:turno_id>', vacunacion_fallida, name="vacunacion_fallida"),
    path('turnos/marcar_inasistencias/', marcar_inasistencias, name='marcar inasistencias'),
]
