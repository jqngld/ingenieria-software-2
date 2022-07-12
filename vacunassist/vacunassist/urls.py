"""vacunassist URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static

from vacunassist.views import *
from administrador.views import *


urlpatterns = [
    path('', home),
    path('admin/pacientes/eliminar/<int:pk>/', paciente_detele_user, name='paciente_detele_user'),
    path('admin/pacientes/asignar_turno/<int:pk>/',admin_asignar_turno, name="asignar_turno"),
    path('admin/pacientes/info/vacunasaplicadas/<int:pk>/', ver_vacunas, name="ver_vacunas"),
    path('admin/personalVacunatorio/cambiarcontrasena/<int:pk>/', PersonalChangePassword.as_view(), name="personal_change_password"),
    path('admin/tablero/', search_dates, name='search_dates'),
    path('admin/pacientes/info/vacunasaplicadas/<int:pk>/', ver_vacunas, name='ver_vacunas'),
    path('admin/personalVacunatorio/eliminar/<int:pk>/', personal_detele_user, name='personal_detele_user'),
    path('admin/personalVacunatorio/cambiarcontrasena/<int:pk>/', PersonalChangePassword.as_view(), name='personal_change_password'),
    path('admin/', admin.site.urls),
    path('administrador/', include('administrador.urls')),
    path('pacientes/', include('pacientes.urls')),
    path('personal_vacunatorio/', include('personalVacunatorio.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)