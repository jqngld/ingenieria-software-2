from django.contrib import admin
from .models import *


# admin.site.register(Usuarios)
admin.site.register(VacunasDetalles)
admin.site.register(PacientesTurnos)
admin.site.register(PacientesDetalles)
admin.site.register(PacientesSolicitudes)
admin.site.register(VacunasAplicadas)