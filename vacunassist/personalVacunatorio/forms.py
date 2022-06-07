from email.policy import default
from django import forms
from django.contrib.auth.forms import UserCreationForm
from pacientes.models import Usuarios


class  PersonalSignIn(forms.Form):
   
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

    email = forms.EmailField(
        max_length=200,
        required=True,
        widget=forms.EmailInput(attrs={'class' : 'form-control', 'placeholder' : 'Email'})
    )
    tipo_usuario = forms.CharField(
        initial='personal',
        widget=forms.TextInput(attrs = {'readonly' : ''}),
    )

    class Meta:
        model = Usuarios
        fields = ('email', 'password1', 'password2', 'tipo_usuario',)



class  devolucionForm(forms.Form):
    
        obervaciones = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs = {'class' : 'form-control','placeholder' : 'observaciones'}))
        
        
        lote = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs = {'class' : 'form-control','placeholder' : 'lote'}))
    

