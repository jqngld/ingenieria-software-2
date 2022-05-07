from django.db import models
from django.contrib.auth.models import User


# A continuación se listarán las tablas que tendrá la base de datos.


class RolesUsuarios(models.Model):

    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo_usuario = models.CharField(max_length=20, blank=False, null=False)

    class Meta:
        db_table = 'roles_usuarios'


class PacientesDetalles(models.Model):

    user_id = models.ForeignKey(RolesUsuarios, on_delete=models.CASCADE)
    paciente_id = models.AutoField(primary_key=True)
    token = models.IntegerField('Token', blank=False, null=False)
    dni = models.IntegerField('DNI', unique=True, blank=False, null=False)
    email = models.EmailField('Mail', unique=True, max_length=254, blank=True, null=False)
    sexo = models.CharField('Sexo', max_length=20, blank=False, null=False)
    nombre = models.CharField('Apellidos', max_length=100, blank=False, null=False)
    apellido = models.CharField('Nombres',max_length=100, blank=False, null=False)
    fecha_nacimiento = models.DateField('Fecha de Nacimiento', blank=False, null=False)
    es_paciente_riesgo = models.BooleanField('Paciente de Riesgo', blank=False, null=False)
    centro_vacunatorio = models.CharField(max_length=50, blank=False, null=False)
    vacuna_f_a_aplicada = models.BooleanField('Vacuna F.A Aplicada', blank=False, null=False)

    class Meta:
        db_table = 'pacientes_detalles'


class VacunasDetalles(models.Model):

    vacuna_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, blank=False, null=False)
    efectividad = models.IntegerField(blank=False, null=False)
    cantidad_dosis = models.CharField(max_length=50, blank=False, null=False)

    class Meta:
        db_table = 'vacunas_detalles'


class PacientesSolicitudes(models.Model):

    solicitud_id = models.AutoField(primary_key=True)
    vacuna_id = models.ForeignKey(VacunasDetalles, on_delete=models.CASCADE)
    paciente_id = models.ForeignKey(PacientesDetalles, on_delete=models.CASCADE)
    fecha_estimada = models.DateField(blank=False, null=False)
    solicitud_aprobada = models.BooleanField(default=False, blank=False, null=False)

    class Meta:
        db_table = 'pacientes_solicitudes'


class PacientesTurnos(models.Model):

    turno_id = models.AutoField(primary_key=True)
    solicitud_id = models.ForeignKey(PacientesSolicitudes, on_delete=models.CASCADE)
    fecha_confirmada = models.DateField(blank=True, null=True)
    turno_perdido = models.BooleanField(default=False, blank=False, null=False)
    turno_pendiente = models.BooleanField(default=True, blank=False, null=False)
    turno_completado = models.BooleanField(default=False, blank=False, null=False)

    class Meta:
        db_table = 'pacientes_turnos'