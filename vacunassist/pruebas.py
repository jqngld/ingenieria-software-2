from vacunassist.wsgi import *
from pacientes.models import *

# Defino los detalles de las vacunas que se aplican
vacuna_covid_1          = VacunasDetalles(nombre = 'COVID-19 (1ra dosis)')
vacuna_covid_2          = VacunasDetalles(nombre = 'COVID-19 (2da dosis)')
vacuna_gripe            = VacunasDetalles(nombre = 'GRIPE')
vacuna_fiebre_amarilla  = VacunasDetalles(nombre = 'FIEBRE AMARILLA')

# Guardo las vacunas en la base de datos
vacuna_covid_1.save()
vacuna_covid_2.save()
vacuna_gripe.save()
vacuna_fiebre_amarilla.save()