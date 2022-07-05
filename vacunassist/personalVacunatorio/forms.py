from email.policy import default
from django import forms
from django.contrib.auth.forms import UserCreationForm
from pacientes.models import Usuarios
from personalVacunatorio.models import PersonalDetalles
from pacientes.models import VacunasAplicadas


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


class PersonalSignUpForm(UserCreationForm):
    """
        Modifique el método __init__ de la clase UserCreationForm, 
        para agregarle los atributos 'placeholder' y 'class' a los
        campos password1 y password2.
    """

    centros = [
        ('Terminal', 'Terminal'),
        ('Cementerio', 'Cementerio'),
        ('Municipalidad', 'Municipalidad'),
    ]

    
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

        return user


class devolucionForm(forms.ModelForm):
    
    class Meta:
        model = VacunasAplicadas
        fields = ['lote', 'observacion']