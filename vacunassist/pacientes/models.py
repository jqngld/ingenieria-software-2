from datetime import datetime
from time import time
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UsuariosManager(BaseUserManager):

    def create_user(self, email, password=None):
        if not email:
            raise ValueError('El usuario debe especificar un correo electrónico.')

        user = self.model(email = self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password=password)
        user.is_admin = True
        user.is_staff = True
        user.tipo_usuario = 'admin'
        user.save()
        return user


class Usuarios(AbstractBaseUser):

    username = None
    first_name = None
    last_name = None

    email = models.EmailField('Mail', unique=True, max_length=254, blank=True, null=False)
    is_active = models.BooleanField(default=True)
    tipo_usuario = models.CharField('Tipo de Usuario', max_length=20, blank=False, null=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    objects = UsuariosManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Usuario'
        db_table = 'usuarios'

    def __str__(self):
        return '%s, %s' % (self.email, self.tipo_usuario)

    def has_perm(self, perm, obj = None):
        return True

    def has_module_perms(self, app_label):
        return True


class PacientesDetalles(models.Model):

    user = models.OneToOneField(Usuarios, on_delete=models.CASCADE)
    paciente_id = models.AutoField(primary_key=True)
    
    dni = models.IntegerField('DNI', unique=True, blank=False, null=False)
    token = models.IntegerField('Token', blank=False, null=False)
    sexo = models.CharField('Sexo', max_length=20, blank=False, null=False)
    nombre = models.CharField('Nombre', max_length=100, blank=False, null=False)
    apellido = models.CharField('Apellido',max_length=100, blank=False, null=False)
    fecha_registro = models.DateTimeField(default=timezone.now)
    fecha_nacimiento = models.DateField('Fecha de Nacimiento', blank=False, null=False)
    es_paciente_riesgo = models.BooleanField('Paciente de Riesgo', default=False)
    centro_vacunatorio = models.CharField('Centro Vacunatorio', max_length=50, blank=False, null=False)


    class Meta:
        verbose_name = 'Detalles Paciente'
        db_table = 'pacientes_detalles'

    def __str__(self) -> str:
        return '%s, %s' % (self.apellido, self.nombre)
    

class VacunasDetalles(models.Model):

    vacuna_id = models.AutoField(primary_key=True)
    nombre = models.CharField('Nombre', max_length=100, blank=False, null=False)
    efectividad = models.CharField('Efectividad', max_length=20, blank=True, null=True)
    cantidad_dosis = models.CharField('Cantidad Dosis', max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = 'Detalles Vacuna'
        db_table = 'vacunas_detalles'

    def __str__(self):
        return '%s' % (self.nombre)


class PacientesSolicitudes(models.Model):

    solicitud_id = models.AutoField(primary_key=True)
    vacuna = models.ForeignKey(VacunasDetalles, on_delete=models.CASCADE)
    paciente = models.ForeignKey(PacientesDetalles, on_delete=models.CASCADE)
    fecha_estimada = models.DateField(blank=False, null=False)
    fecha_solicitud = models.DateField(default=datetime.today)
    solicitud_aprobada = models.BooleanField(default=False, blank=False, null=False)
    centro_vacunatorio = models.CharField('Centro Vacunatorio', max_length=50, blank=False, null=False)
    
    class Meta:
        verbose_name = 'Solicitudes Paciente'
        db_table = 'pacientes_solicitudes'

    def __str__(self) -> str:
        return '%s - %s: %s' % (self.paciente, self.paciente.dni, self.vacuna)


class PacientesTurnos(models.Model):

    turno_id = models.AutoField(primary_key=True)
    solicitud = models.ForeignKey(PacientesSolicitudes, on_delete=models.CASCADE)
    fecha_confirmada = models.DateField(blank=True, null=True)
    turno_perdido = models.BooleanField(default=False, blank=False, null=False)
    turno_pendiente = models.BooleanField(default=True, blank=False, null=False)
    turno_completado = models.BooleanField(default=False, blank=False, null=False)

    class Meta:
        verbose_name = 'Turnos Paciente'
        db_table = 'pacientes_turnos'

    def __str__(self) -> str:
        return '%s - %s: %s' % (self.solicitud.paciente, self.solicitud.paciente.dni, self.solicitud.vacuna.nombre)


class VacunasAplicadas(models.Model):
    vacuna = models.ForeignKey(VacunasDetalles, on_delete=models.CASCADE)
    paciente = models.ForeignKey(PacientesDetalles, on_delete=models.CASCADE) 
    lote = models.CharField('lote', max_length=100, blank=False, null=False, default=" ")
    observacion = models.CharField('observacion', max_length=100, blank=True, null=True)
    fecha_vacunacion = models.DateField('Fecha de Vacunacion', blank=False)

    class Meta:
        verbose_name = 'Vacunas Aplicada'
        db_table = 'vacunas_aplicadas'

    def __str__(self) -> str:
        return '%s - %s: %s' % (self.paciente.dni, self.vacuna.nombre, self.fecha_vacunacion)