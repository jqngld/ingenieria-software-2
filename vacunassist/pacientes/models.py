from django.db import models
from django.contrib.auth.models import User


class UsersDetails(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type_id = models.IntegerField(blank=False, null=False)
    description = models.CharField(max_length=20, blank=False, null=False)

    class Meta:
        db_table = 'users_details'


class VaccinationCenters(models.Model):

    vaccination_center_id = models.AutoField(primary_key=True)
    zone_description = models.CharField('Centro de Preferencia', max_length=200, blank=False, null=False)

    class Meta:
        db_table = 'vaccination_centers'


class PatientsDetails(models.Model):

    patient_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UsersDetails, on_delete=models.CASCADE)
    dni = models.IntegerField('DNI', unique=True, blank=False, null=False)
    email = models.EmailField('Mail', unique=True, max_length=254, blank=True, null=False)
    gender = models.CharField('Sexo', max_length=20, blank=False, null=False)
    last_name = models.CharField('Nombres',max_length=100, blank=False, null=False)
    first_name = models.CharField('Apellidos', max_length=100, blank=False, null=False)
    birth_date = models.DateField('Fecha de Nacimiento', blank=False, null=False)
    security_token = models.IntegerField('Token', blank=False, null=False)
    is_risk_patient = models.BooleanField('Paciente de Riesgo', blank=False, null=False)
    vaccination_center = models.ForeignKey(VaccinationCenters, on_delete=models.CASCADE)
    has_yellow_fever_vaccine = models.BooleanField('Vacuna F.A Aplicada', blank=False, null=False)

    class Meta:
        db_table = 'patients_details'


class VaccinesDetails(models.Model):

    vaccine_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=False, null=False)
    duration = models.CharField(max_length=50, blank=False, null=False)
    dose_amount = models.IntegerField(blank=False, null=False)

    class Meta:
        db_table = 'vaccines_details'


class PatientsRequests(models.Model):

    request_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(PatientsDetails, on_delete=models.CASCADE)
    vaccine = models.ForeignKey(VaccinesDetails, on_delete=models.CASCADE)
    is_confirmed = models.BooleanField(default=False, blank=False, null=False)
    estimated_date = models.DateField(blank=False, null=False)

    class Meta:
        db_table = 'patients_requests'


class PatientsShifts(models.Model):

    shift_id = models.AutoField(primary_key=True)
    request = models.ForeignKey(PatientsRequests, on_delete=models.CASCADE)
    confirmed_shift_date = models.DateField(blank=True, null=True)
    flag_done_shift = models.BooleanField(default=False, blank=False, null=False)
    flag_missed_shift = models.BooleanField(default=False, blank=False, null=False)
    flag_waiting_shift = models.BooleanField(default=True, blank=False, null=False)

    class Meta:
        db_table = 'patients_shifts'