from django.contrib import admin
from .forms import PersonalSignUpForm
from pacientes.models import Usuarios

# class UserPersonalForm(forms.ModelForm):

#     class Meta:
#         model = Usuarios
#         exclude = ['last_login', 'is_staff', 'is_admin']


@admin.register(Usuarios)
class PersonalAdmin(admin.ModelAdmin):
    form = PersonalSignUpForm