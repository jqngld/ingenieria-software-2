from django.db import models

# Create your models here.

class PersonalDetalles(models.Model):

    personal_id = models.AutoField(primary_key=True)
    centro_vacunatorio = models.CharField('Centro Vacunatorio', max_length=50, blank=False, null=False)
    


    class Meta:
        verbose_name = 'Detalles Personal'
        db_table = 'personal_detalles'
