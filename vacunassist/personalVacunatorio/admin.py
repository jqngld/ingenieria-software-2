from django.contrib import admin
from .forms import PersonalSignUpForm
from pacientes.models import Usuarios


@admin.register(Usuarios)
class PersonalAdmin(admin.ModelAdmin):
    form = PersonalSignUpForm