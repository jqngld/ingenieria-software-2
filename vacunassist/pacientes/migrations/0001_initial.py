# Generated by Django 4.0.3 on 2022-06-01 01:05

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Usuarios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(blank=True, max_length=254, unique=True, verbose_name='Mail')),
                ('is_active', models.BooleanField(default=True)),
                ('tipo_usuario', models.CharField(max_length=20, verbose_name='Tipo de Usuario')),
            ],
            options={
                'verbose_name': 'Usuario',
                'db_table': 'usuarios',
            },
        ),
        migrations.CreateModel(
            name='PacientesDetalles',
            fields=[
                ('paciente_id', models.AutoField(primary_key=True, serialize=False)),
                ('dni', models.IntegerField(unique=True, verbose_name='DNI')),
                ('token', models.IntegerField(verbose_name='Token')),
                ('sexo', models.CharField(max_length=20, verbose_name='Sexo')),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre')),
                ('apellido', models.CharField(max_length=100, verbose_name='Apellido')),
                ('fecha_registro', models.DateTimeField(default=django.utils.timezone.now)),
                ('fecha_nacimiento', models.DateField(verbose_name='Fecha de Nacimiento')),
                ('es_paciente_riesgo', models.BooleanField(default=False, verbose_name='Paciente de Riesgo')),
                ('centro_vacunatorio', models.CharField(max_length=50, verbose_name='Centro Vacunatorio')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Detalles Paciente',
                'db_table': 'pacientes_detalles',
            },
        ),
        migrations.CreateModel(
            name='PacientesSolicitudes',
            fields=[
                ('solicitud_id', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_estimada', models.DateField()),
                ('fecha_solicitud', models.DateField(default=datetime.datetime.today)),
                ('solicitud_aprobada', models.BooleanField(default=False)),
                ('centro_vacunatorio', models.CharField(max_length=50, verbose_name='Centro Vacunatorio')),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pacientes.pacientesdetalles')),
            ],
            options={
                'verbose_name': 'Solicitudes Paciente',
                'db_table': 'pacientes_solicitudes',
            },
        ),
        migrations.CreateModel(
            name='VacunasDetalles',
            fields=[
                ('vacuna_id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre')),
                ('efectividad', models.CharField(blank=True, max_length=20, null=True, verbose_name='Efectividad')),
                ('cantidad_dosis', models.CharField(blank=True, max_length=50, null=True, verbose_name='Cantidad Dosis')),
            ],
            options={
                'verbose_name': 'Detalles Vacuna',
                'db_table': 'vacunas_detalles',
            },
        ),
        migrations.CreateModel(
            name='VacunasAplicadas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_vacunacion', models.DateField(verbose_name='Fecha de Vacunacion')),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pacientes.pacientesdetalles')),
                ('vacuna', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pacientes.vacunasdetalles')),
            ],
            options={
                'verbose_name': 'Vacunas Aplicada',
                'db_table': 'vacunas_aplicadas',
            },
        ),
        migrations.CreateModel(
            name='PacientesTurnos',
            fields=[
                ('turno_id', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_confirmada', models.DateField(blank=True, null=True)),
                ('turno_perdido', models.BooleanField(default=False)),
                ('turno_pendiente', models.BooleanField(default=True)),
                ('turno_completado', models.BooleanField(default=False)),
                ('solicitud', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pacientes.pacientessolicitudes')),
            ],
            options={
                'verbose_name': 'Turnos Paciente',
                'db_table': 'pacientes_turnos',
            },
        ),
        migrations.AddField(
            model_name='pacientessolicitudes',
            name='vacuna',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pacientes.vacunasdetalles'),
        ),
    ]
