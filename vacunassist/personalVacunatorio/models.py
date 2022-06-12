from django.db import models
from pacientes.models import Usuarios


class PersonalDetalles(models.Model):

    user = models.OneToOneField(Usuarios, on_delete=models.CASCADE)
    personal_id = models.AutoField(primary_key=True)
    centro_vacunatorio = models.CharField('Centro Vacunatorio', max_length=50, blank=False, null=False)
    
    class Meta:
        verbose_name = 'Detalles Personal'
        db_table = 'personal_detalles'
