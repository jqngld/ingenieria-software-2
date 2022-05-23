from re import template
from django.urls import path
from pacientes.views import *
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', home, name='home'),
    path('registro/', signup, name='signup'),
    path('inicio_sesion/', login, name='login'),
    path('cerrar_sesion', logout, name='logout'),
    path('login_error/', login_error, name='login_error'),
    path('mi_perfil/', view_profile, name='view_profile'),
    path('editar_perfil/',editar_perfil, name='editar_perfil'),
    path('contraseña/', cambiarPassword.as_view(template_name='pacientes/cambiar-contraseña.html')),
    path('password_change/done/',auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    #path('editar_perfil/', editar_perfil.as_view()), 
    path('mis_turnos/', listar_turnos, name="listar_turnos"),
    path('mis_vacunas/', listar_vacunas, name="listar_vacunas"),
    path('mis_solicitudes/', listar_solicitudes, name="listar_solicitudes"),
    path('inicio_pacientes/', inicio_pacientes, name='inicio_pacientes'),
    path('mis_vacunas/descargar_comprobante/<int:vacuna_id>', descargar_comprobante.as_view(), name="descargar_comprobante")
] 
