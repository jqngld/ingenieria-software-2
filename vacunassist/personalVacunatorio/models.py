from django.db import models
from django.utils import timezone
from pacientes.models import Usuarios


class PersonalDetalles(models.Model):

    user = models.OneToOneField(Usuarios, on_delete=models.CASCADE)
    personal_id = models.AutoField(primary_key=True)

    nombre = models.CharField('Nombre', max_length=100, blank=False, null=False, default='m')
    apellido = models.CharField('Apellido', max_length=100, blank=False, null=False, default='m')
    numero_telefono = models.CharField('Número Teléfono', max_length=20)
    fecha_nacimiento = models.DateField('Fecha de Nacimiento', blank=False, null=False)
    centro_vacunatorio = models.CharField('Centro Vacunatorio', max_length=50, blank=False, null=False)
    
    class Meta:
        verbose_name = 'Detalles Personal'
        db_table = 'personal_detalles'
