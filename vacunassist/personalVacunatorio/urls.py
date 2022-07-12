from django.urls import path
from personalVacunatorio.views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', home_personal, name='home_personal'),
    path('turnos/', listar_turnos_diarios, name='listar_turnos_diarios'),
    path('turnos_ausentes/', listar_historial_ausentes, name='listar_historial_ausentes'),
    path('turnos_atendidos/', listar_historial_atendidos, name='listar_historial_atendidos'),
    path('inicio_sesion/', login_personal, name='login_personal'),
    path('cerrar_sesion/', logout_personal, name='logout_personal'),
    path('login_error/', login_error_personal, name='login_error_personal'),
    path('devolucion/<int:vacuna_aplicada>/', devolucion, name='devolucion'),
    path('turnos/vacunacion_exitosa/<int:turno_id>/<int:paciente_dni>/<str:vacuna_nombre>/', vacunacion_exitosa, name="vacunacion_exitosa"),
    path('turnos/vacunacion_fallida/<int:turno_id>', vacunacion_fallida, name="vacunacion_fallida"),
    path('turnos/marcar_inasistencias/', marcar_inasistencias, name='marcar inasistencias'),
    path('restablecer-contrasenia/',restPasswordPer, name='reset_passwordPer'),
    path('restablecer-contrasenia-hecho/',restDone, name='restablecer-contrasenia-hecho'),
    path('reset/<uidb64>/<token>', restPasswordConfirm.as_view(template_name='personalVacunatorio/rest-contra-conf.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="personalVacunatorio/password_reset_confirm.html"), name='password_reset_complete'),
]
