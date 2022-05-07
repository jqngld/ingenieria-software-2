from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class RolesUsuarios(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo_usuario = models.CharField(max_length=20, blank=False, null=False)

    class Meta:
        verbose_name = 'Roles Usuario'
        db_table = 'roles_usuarios'

    def __str__(self) -> str:
        return '%s: %s' % (self.tipo_usuario, self.user.username)


class PacientesDetalles(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    paciente_id = models.AutoField(primary_key=True)
    token = models.IntegerField('Token', blank=False, null=False)
    dni = models.IntegerField('DNI', unique=True, blank=False, null=False)
    email = models.EmailField('Mail', unique=True, max_length=254, blank=True, null=False)
    sexo = models.CharField('Sexo', max_length=20, blank=False, null=False)
    nombre = models.CharField('Nombre', max_length=100, blank=False, null=False)
    apellido = models.CharField('Apellido',max_length=100, blank=False, null=False)
    fecha_registro = models.DateTimeField(default=timezone.now)
    fecha_nacimiento = models.DateField('Fecha de Nacimiento', blank=False, null=False)
    es_paciente_riesgo = models.BooleanField('Paciente de Riesgo', default=False, blank=False, null=False)
    centro_vacunatorio = models.CharField('Centro Vacunatorio', max_length=50, blank=False, null=False)
    vacuna_f_a_aplicada = models.BooleanField('Vacuna F.A Aplicada', blank=False, null=False)

    class Meta:
        verbose_name = 'Detalles Paciente'
        db_table = 'pacientes_detalles'

    def __str__(self):
        return '%s, %s' % (self.apellido, self.nombre)


class VacunasDetalles(models.Model):

    vacuna_id = models.AutoField(primary_key=True)
    nombre = models.CharField('Nombre', max_length=100, blank=False, null=False)
    efectividad = models.CharField('Efectividad', max_length=20, blank=False, null=False)
    cantidad_dosis = models.CharField('Cantidad Dosis', max_length=50, blank=False, null=False)

    class Meta:
        verbose_name = 'Detalles Vacuna'
        db_table = 'vacunas_detalles'

    def __str__(self):
        return '%s' % (self.nombre)


class PacientesSolicitudes(models.Model):

    solicitud_id = models.AutoField(primary_key=True)
    vacuna_id = models.ForeignKey(VacunasDetalles, on_delete=models.CASCADE)
    paciente_id = models.ForeignKey(PacientesDetalles, on_delete=models.CASCADE)
    fecha_estimada = models.DateField(blank=False, null=False)
    solicitud_aprobada = models.BooleanField(default=False, blank=False, null=False)

    class Meta:
        verbose_name = 'Solicitudes Paciente'
        db_table = 'pacientes_solicitudes'

    def __str__(self) -> str:
        return '%s - %s: %s' % (self.paciente_id, self.paciente_id.dni, self.vacuna_id)


class PacientesTurnos(models.Model):

    turno_id = models.AutoField(primary_key=True)
    solicitud_id = models.ForeignKey(PacientesSolicitudes, on_delete=models.CASCADE)
    fecha_confirmada = models.DateField(blank=True, null=True)
    turno_perdido = models.BooleanField(default=False, blank=False, null=False)
    turno_pendiente = models.BooleanField(default=True, blank=False, null=False)
    turno_completado = models.BooleanField(default=False, blank=False, null=False)

    class Meta:
        verbose_name = 'Turnos Paciente'
        db_table = 'pacientes_turnos'

    def __str__(self) -> str:
        return '%s - %s: %s' % (self.solicitud_id.paciente_id, self.solicitud_id.vacuna_id, self.fecha_confirmada)

