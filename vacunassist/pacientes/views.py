import email
from pacientes.models import Usuarios, PacientesDetalles
from email import message
from lib2to3.pgen2 import token
from pyexpat.errors import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .forms import UserSignUpForm,UserSign
from django.contrib.auth.forms import AuthenticationForm , UserCreationForm
from django import forms
from django.contrib.auth import authenticate,login
from django.contrib import messages
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import authenticate, login as patient_login
from django.contrib.auth.decorators import login_required

def home(request):

    return render(request, 'pacientes/index.html')


def mail(request):
    return render(request, 'pacientes/multiple_steps_form.html')    
 

def login(request):   
    if request.method == "POST":
       form = UserSign(data=request.POST)
       if form.is_valid(): 
            mail= form.cleaned_data.get("email")
            contraseña= form.cleaned_data.get("password")
            token = form.cleaned_data.get("token")
            user= authenticate(email = mail,password = contraseña)
            if user is not None and PacientesDetalles.objects.filter(token=token,user=user).exists():
                patient_login(request, user)
                return redirect('/pacientes/')
            else:
                 messages.error(request, "usuario no valido")  
       else: 
             messages.error(request, "informacion")                     
    form = UserSign()     
    context = {'form' : form}
    return render(request, 'pacientes/login.html', context)


def signup(request):

    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/pacientes/')
    else:
        form = UserSignUpForm()

    context = {'form' : form}
    return render(request, 'pacientes/signup.html', context)


#def viewProfile(request): proxima implementación
    users = PacientesDetalles.objects.all()
    return render(request, "pacientes/list_users.html", {"usrs": users})