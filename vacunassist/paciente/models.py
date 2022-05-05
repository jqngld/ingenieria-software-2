from django.db import models


class Paciente(models.Model):

    patient_id = models.AutoField(primary_key=True)
    dni = models.IntegerField(blank=False, null=False)
    email = models.EmailField(max_length=200, blank=False, null=False)
    gender = models.CharField(max_length=20, blank=False, null=False)
    last_name = models.CharField(max_length=100, blank=False, null=False)
    first_name = models.CharField(max_length=100, blank=False, null=False)
    birth_date = models.DateField(blank=False, null=False)
    is_risk_patient = models.BooleanField(blank=False, null=False)
    has_yellow_fever_vaccine = models.BooleanField(blank=False, null=False)