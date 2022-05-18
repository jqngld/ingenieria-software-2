from django import forms
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.forms import UserCreationForm
from pacientes.models import Usuarios, PacientesDetalles
from .models import Usuarios
from vacunassist import settings
import os
import string
import random
from datetime import datetime
from email.mime.image import MIMEImage


class  UserSign(forms.Form):
   email = forms.EmailField(max_length=200, required=True)
   password = forms.CharField(label="Contraseña", widget=forms.PasswordInput())
   token = forms.IntegerField(label='token', required=True)

class UserSignUpForm(UserCreationForm):
    """
        Modifique el método __init__ de la clase UserCreationForm, 
        para agregarle los atributos 'placeholder' y 'class' a los
        campos password1 y password2.
    """

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

    nombre = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs = {'class' : 'form-control','placeholder' : 'Nombre'}))
    apellido = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs = {'class' : 'form-control','placeholder' : 'Apellido'}))
    email = forms.EmailField(
        max_length=200,
        required=True,
        widget=forms.EmailInput(attrs={'class' : 'form-control', 'placeholder' : 'Email'}))

    dni = forms.IntegerField(
        label='DNI',
        required=True,
        widget=forms.NumberInput(attrs = {'class' : 'form-control','placeholder' : 'DNI'}))
    sexo = forms.ChoiceField(
        choices=generos,
        required=True,
        label="Género",
        widget=forms.Select(attrs={'class' : 'form-control', 'placeholder' : 'Sexo'}))
    dia_nacimiento = forms.IntegerField(
        label='Día',
        widget=forms.NumberInput(attrs = {'class' : 'form-control','placeholder' : 'Día'}))
    mes_nacimiento = forms.ChoiceField(
        choices=meses,
        required=True,
        label="Mes",
        widget=forms.Select(attrs={'class' : 'form-control','placeholder' : 'Mes'}))
    ano_nacimiento = forms.IntegerField(
        label='Año',
        widget=forms.NumberInput(attrs = {'class' : 'form-control','placeholder' : 'Año'})
    )
    centro_vacunatorio = forms.ChoiceField(
        choices=centros,
        required=True,
        label="Centro vacunatorio",
        widget=forms.Select(attrs = {'class' : 'form-control','placeholder' : 'Centro Vacunatorio'})
    )
    es_paciente_riesgo = forms.BooleanField(required=False, label='Respecto a la vacuna COVID-19, ¿es paciente de riesgo?')
    
    vacuna_covid = forms.BooleanField(
        required=False,
        label='COVID-19',
        widget=forms.CheckboxInput(attrs={'OnClick': 'disableCovidField();'})
    )
    fecha_vacunacion_covid = forms.DateField(
        required=False,
        label='Fecha aplicación',
        widget=forms.DateInput(attrs = {'disabled' : 'true', 'type': 'date', 'class' : 'form-control', 'placeholder' : 'Fecha Vacunación'})
    )

    vacuna_gripe = forms.BooleanField(
        required=False,
        label='GRIPE',
        widget=forms.CheckboxInput(attrs={'OnClick': 'disableGripeField();'})
    )
    fecha_vacunacion_gripe = forms.DateField(
        required=False,
        label='Fecha aplicación',
        widget=forms.DateInput(attrs = {'disabled' : 'true', 'type': 'date', 'class': 'form-control','placeholder' : 'Fecha Vacunación'})
    )
    
    vacuna_fa = forms.BooleanField(
        required=False,
        label='FIEBRE AMARILLA', widget=forms.CheckboxInput(attrs={'OnClick': 'disableFAField();'})
    )
    fecha_vacunacion_fa = forms.DateField(
        required=False,
        label='Fecha aplicación',
        widget=forms.DateInput(attrs = {'disabled' : 'true', 'type': 'date', 'class' : 'form-control','placeholder' : 'Fecha Vacunación'})
    )

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



    def send_register_email(self, token):
        subject = 'Registro de Usuario Exitoso.'
        from_email = 'VacunAssist <%s>' % (settings.EMAIL_HOST_USER)
        to_email = '%s' % (self.cleaned_data['email'])
        reply_to_email = 'noreply@vacunassist.com'

        image_dir = 'static/img'
        image_name = 'vacunassist-logo.png'

        context = {
                    'nombre' : self.cleaned_data.get('nombre'),
                    'token'  : token
                    }

        text_content = get_template('pacientes/mail_bienvenida.txt')
        html_content = get_template('pacientes/mail_bienvenida.html')
        text_content = text_content.render(context)
        html_content = html_content.render(context)

        email = EmailMultiAlternatives(subject, text_content, from_email, to=[to_email,], reply_to=[reply_to_email,])
        email.mixed_subtype = 'related'
        email.content_subtype = 'html'
        email.attach_alternative(html_content, 'text/html')

        file_path = os.path.join(image_dir, image_name)
        with open(file_path, 'rb') as f:
            image = MIMEImage(f.read())
            image.add_header('Content-ID', '<%s>' % (image_name))
            image.add_header('Content-Disposition', 'inline', filename=image_name)
            email.attach(image)

        email.send(fail_silently=False)

    def clean_dni(self):
        dni = self.cleaned_data.get('dni')
        if PacientesDetalles.objects.filter(dni=dni).exists():
            raise forms.ValidationError('Ya existe un usuario con este DNI.')
        return dni

    def validar_email(self, email):
        if Usuarios.objects.filter(email=email).exists():
            raise forms.ValidationError('Ya existe un usuario con este Email.')
        return email

    def save(self, commit=True):
        if not commit:
            raise NotImplementedError("Can't create User and UserProfile without database save")
        user = super(UserSignUpForm, self).save(commit=True)
        user.tipo_usuario = 'paciente'
        user.save()
        token = self.generate_token()
        patient_details = PacientesDetalles(
            user=user,
            token = token,
            dni = self.cleaned_data['dni'],
            sexo = self.cleaned_data['sexo'],
            nombre = self.cleaned_data['nombre'], 
            apellido = self.cleaned_data['apellido'],
            fecha_nacimiento = datetime(int(self.cleaned_data['ano_nacimiento']), int(self.cleaned_data['mes_nacimiento']), int(self.cleaned_data['dia_nacimiento'])),
            es_paciente_riesgo = self.cleaned_data['es_paciente_riesgo'],
            centro_vacunatorio = self.cleaned_data['centro_vacunatorio']
        )
        patient_details.save()
        self.send_register_email(token)
        return user, patient_details
