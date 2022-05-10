from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from pacientes.models import Usuarios, PacientesDetalles
from .models import Usuarios
import string
import random
from datetime import datetime


class UserSignUpForm(UserCreationForm):

    generos = [
        ('Mujer' , 'Mujer'),
        ('Hombre', 'Hombre'),
        ('N/A'  , 'Prefiero no decirlo'),
        ('Otro'  , 'Otro'),
    ]

    meses = [
        (1, 'Enero')     , (2, 'Febrero'),
        (3, 'Marzo')     , (4, 'Abril'),
        (5, 'Mayo')      , (6, 'Junio'),
        (7, 'Julio')     , (8, 'Agosto'),
        (9, 'Septiembre'), (10, 'Octubre'),
        (11,'Noviembre') , (12, 'Diciembre'),
    ]

    centros = [
        ('Terminal', 'Terminal'),
        ('Cementerio', 'Cementerio'),
        ('Municipalidad', 'Municipalidad'),
    ]

    nombre = forms.CharField(max_length=100, required=True)
    apellido = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(max_length=200, required=True)
    
    dni = forms.IntegerField(label='DNI', required=True)
    sexo = forms.ChoiceField(choices=generos, required=True, label="Género")
    dia_nacimiento = forms.IntegerField(label='Día')
    mes_nacimiento = forms.ChoiceField(choices=meses, required=True, label="Mes")
    ano_nacimiento = forms.IntegerField(label='Año')
    centro_vacunatorio = forms.ChoiceField(choices=centros, required=True, label="Centro vacunatorio")
    es_paciente_riesgo = forms.BooleanField(required=False, label='¿Es paciente de riesgo?')
    
    vacuna_covid = forms.BooleanField(required=False, label='¿Se aplicó la vacuna COVID-19?')
    fecha_vacunacion_covid = forms.DateField(required=False)
    
    vacuna_gripe = forms.BooleanField(required=False, label='¿Se aplicó la vacuna GRIPE?')
    fecha_vacunacion_gripe = forms.DateField(required=False)
    
    vacuna_fa = forms.BooleanField(required=False, label='¿Se aplicó la vacuna FIEBRE AMARILLA?')
    fecha_vacunacion_fa = forms.DateField(required=False)

    class Meta:
        model = Usuarios
        fields = ('nombre', 'apellido', 'email',
                  'password1', 'password2', 'dni', 'sexo',
                  'dia_nacimiento', 'mes_nacimiento', 'ano_nacimiento',
                  'centro_vacunatorio', 'es_paciente_riesgo',
                  'vacuna_covid', 'fecha_vacunacion_covid',
                  'vacuna_gripe', 'fecha_vacunacion_gripe',
                  'vacuna_fa', 'fecha_vacunacion_fa'
                )

    def generate_token(self):   
        length_of_string = 4
        return ''.join(random.choice(string.digits) for _ in range(length_of_string))

    def save(self, commit=True):
        if not commit:
            raise NotImplementedError("Can't create User and UserProfile without database save")
        user = super(UserSignUpForm, self).save(commit=True)
        user.tipo_usuario = 'paciente'
        user.save()
        patient_details = PacientesDetalles(
            user=user,
            token = self.generate_token(),
            dni = self.cleaned_data['dni'],
            sexo = self.cleaned_data['sexo'],
            nombre = self.cleaned_data['nombre'], 
            apellido = self.cleaned_data['apellido'],
            fecha_nacimiento = datetime(int(self.cleaned_data['ano_nacimiento']), int(self.cleaned_data['mes_nacimiento']), int(self.cleaned_data['dia_nacimiento'])),
            es_paciente_riesgo = self.cleaned_data['es_paciente_riesgo'],
            centro_vacunatorio = self.cleaned_data['centro_vacunatorio']
        )
        patient_details.save()
        return user, patient_details
