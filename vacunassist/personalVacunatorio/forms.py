
from django import forms
from django.contrib.auth.forms import UserCreationForm
from pacientes.models import Usuarios
from personalVacunatorio.models import PersonalDetalles
from pacientes.models import VacunasAplicadas
from email.mime.image import MIMEImage
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from vacunassist import settings
import os


from django.contrib.auth.hashers import check_password


centros = [
        ('Terminal', 'Terminal'),
        ('Cementerio', 'Cementerio'),
        ('Municipalidad', 'Municipalidad'),
    ]


class PersonalSignIn(forms.Form):
   
    email = forms.EmailField(
        max_length=200,
        required=True,
        widget=forms.EmailInput(attrs={'class' : 'form-control', 'placeholder' : 'Email'})
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput()
    )


class PersonalChangeForm(forms.ModelForm):
    
    nombre = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs = {'class' : 'form-control','placeholder' : 'Nombre'})
    )
    apellido = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs = {'class' : 'form-control','placeholder' : 'Apellido'})
    )
    numero_telefono = forms.IntegerField(
        label='Número Teléfono',
        required=False,
        widget=forms.TextInput(attrs = {'class' : 'form-control','placeholder' : 'Número de teléfono'})
    )
    fecha_nacimiento = forms.DateField(
        required=True,
        label='Fecha Nacimiento',
        widget=forms.DateInput(attrs = {'type': 'date', 'class' : 'form-control', 'placeholder' : 'Fecha de Nacimiento'})
    )
    email = forms.EmailField(
        max_length=200,
        required=True,
        widget=forms.EmailInput(attrs={'class' : 'form-control', 'placeholder' : 'Email'})
    )
    centro_vacunatorio = forms.ChoiceField(
        choices=centros,
        required=True,
        label="Centro vacunatorio",
        widget=forms.Select(attrs = {'class' : 'form-control','placeholder' : 'Centro Vacunatorio'})
    )


    # redefinir este método para que se pueda actualizar sin problemas
    def save(self, commit=True):
        # if not commit:
        #     raise NotImplementedError("Can't create User and UserProfile without database save")
        user = super(PersonalChangeForm, self).save(commit=False)
        user.tipo_usuario = 'personal'
        user.email = self.cleaned_data['email']
        user.save()

        personal_details = PersonalDetalles.objects.get(user=user)
        personal_details.nombre             = self.cleaned_data['nombre']
        personal_details.apellido           = self.cleaned_data['apellido']
        personal_details.numero_telefono    = self.cleaned_data['numero_telefono']
        personal_details.fecha_nacimiento   = self.cleaned_data['fecha_nacimiento']
        personal_details.centro_vacunatorio = self.cleaned_data['centro_vacunatorio']
        personal_details.save()

        return user


    class Meta:
        model = PersonalDetalles
        fields = ('nombre', 'apellido', 'numero_telefono', 'fecha_nacimiento', 'email', 'centro_vacunatorio')


class PersonalSignUpForm(UserCreationForm):
    """
        Modifique el método __init__ de la clase UserCreationForm, 
        para agregarle los atributos 'placeholder' y 'class' a los
        campos password1 y password2.
    """

    nombre = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs = {'class' : 'form-control','placeholder' : 'Nombre'})
    )
    apellido = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs = {'class' : 'form-control','placeholder' : 'Apellido'})
    )
    numero_telefono = forms.IntegerField(
        label='Número Teléfono',
        required=False,
        widget=forms.TextInput(attrs = {'class' : 'form-control','placeholder' : 'Número de teléfono'})
    )
    fecha_nacimiento = forms.DateField(
        required=True,
        label='Fecha Nacimiento',
        widget=forms.DateInput(attrs = {'type': 'date', 'class' : 'form-control', 'placeholder' : 'Fecha de Nacimiento'})
    )
    email = forms.EmailField(
        max_length=200,
        required=True,
        widget=forms.EmailInput(attrs={'class' : 'form-control', 'placeholder' : 'Email'})
    )
    centro_vacunatorio = forms.ChoiceField(
        choices=centros,
        required=True,
        label="Centro vacunatorio",
        widget=forms.Select(attrs = {'class' : 'form-control','placeholder' : 'Centro Vacunatorio'})
    )

    class Meta:
        model = Usuarios
        fields = ('nombre', 'apellido', 'numero_telefono', 'fecha_nacimiento',
                  'email', 'password1', 'password2', 'centro_vacunatorio',)


    def send_register_email(self):
        '''Se envía un mail al correo del usuario paciente registrado con el token que
        se generó para utilizar en el inicio de sesión.'''

        subject = 'Registro de Usuario Exitoso.'
        from_email = 'VacunAssist <%s>' % (settings.EMAIL_HOST_USER)
        to_email = '%s' % (self.cleaned_data['email'])
        reply_to_email = 'noreply@vacunassist.com'

        image_dir = 'static/img'
        image_name = 'vacunassist-logo.png'

        context = {
                    'nombre' : self.cleaned_data.get('nombre'),
                    }

        text_content = get_template('personalVacunatorio/mail_bienvenida.txt')
        html_content = get_template('personalVacunatorio/mail_bienvenida.html')
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

    def save(self, commit=True):
        # if not commit:
        #     raise NotImplementedError("Can't create User and UserProfile without database save")
        user = super(PersonalSignUpForm, self).save(commit=True)
        user.tipo_usuario = 'personal'
        user.save()
        
        if PersonalDetalles.objects.filter(user=user).exists():
            personal_details = PersonalDetalles.objects.get(user=user)
            personal_details.nombre             = self.cleaned_data['nombre']
            personal_details.apellido           = self.cleaned_data['apellido']
            personal_details.numero_telefono    = self.cleaned_data['numero_telefono']
            personal_details.fecha_nacimiento   = self.cleaned_data['fecha_nacimiento']
            personal_details.centro_vacunatorio = self.cleaned_data['centro_vacunatorio']
        else:
            personal_details = PersonalDetalles(
                user = user,
                nombre             = self.cleaned_data['nombre'],
                apellido           = self.cleaned_data['apellido'],
                numero_telefono    = self.cleaned_data['numero_telefono'],
                fecha_nacimiento   = self.cleaned_data['fecha_nacimiento'],
                centro_vacunatorio = self.cleaned_data['centro_vacunatorio'],
            )
        personal_details.save()
        self.send_register_email()

        return user


class devolucionForm(forms.Form):
    
    lote = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs = {'class' : 'form-control','placeholder' : 'Lote'})
    )

    observacion = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs = {'class' : 'form-control','placeholder' : 'Observacion'})
    )