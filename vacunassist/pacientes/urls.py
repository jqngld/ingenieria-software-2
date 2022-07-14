from django.urls import path
from pacientes.views import *
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', home, name='home'),
    path('registro1/', signup1, name='signup1'),
    path('registro2/', signup2, name='signup2'),
    path('inicio_sesion/', login, name='login'),
    path('cerrar_sesion', logout, name='logout'),
    path('login_error/', login_error, name='login_error'),
    path('mi_perfil/', view_profile, name='view_profile'),
    path('editar_perfil/',editar_perfil, name='editar_perfil'),
    path('contraseña/', cambiarPassword.as_view(template_name='pacientes/cambiar-contraseña.html')),
    path('password_change/done/',auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('mis_turnos/', listar_turnos, name="listar_turnos"),
    path('mis_vacunas/', listar_vacunas, name="listar_vacunas"),
    path('mis_solicitudes/', listar_solicitudes, name="listar_solicitudes"),
    path('mis_solicitudes/solicitud_fiebre_amarilla/', solicitud_fiebre_amarilla, name="solicitud_fiebre_amarilla"),
    path('inicio_pacientes/', inicio_pacientes, name='inicio_pacientes'),
    path('mis_vacunas/descargar_comprobante/<int:vacuna_id>', descargar_comprobante.as_view(), name="descargar_comprobante"),
    #path('reset_password/', restPassword.as_view(template_name='pacientes/restablecer-contrasenia.html'), name='password_reset'),
    path('restablecer-contrasenia/',restPassword, name='reset_password'),
    path('restablecer-contrasenia-hecho/',restDone, name='restablecer-contrasenia-hecho'),
    path('reset/<uidb64>/<token>', restPasswordConfirm.as_view(template_name='pacientes/rest-contra-conf.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="pacientes/password_reset_confirm.html"), name='password_reset_complete'),
] 
