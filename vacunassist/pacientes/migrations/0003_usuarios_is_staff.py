# Generated by Django 4.0.3 on 2022-06-01 01:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pacientes', '0002_usuarios_is_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuarios',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
    ]
