from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate
from django.contrib.auth import logout as personal_logout
from django.contrib.auth import login as personal_auth_login
from django.contrib.auth.decorators import login_required

from pacientes.models import *
from .forms import *

from datetime import datetime 


def home_personal(request):
    return render(request, 'personalVacunatorio/index.html')


def login_error_personal(request):
    return HttpResponse('Usuario no logueado.')


@login_required(login_url='/personal_vacunatorio/login_error/')
def logout_personal(request):
    personal_logout(request)

    return redirect('/personal_vacunatorio/')


def login_personal(request):
    if request.method == "POST":
       form = PersonalSignIn(data=request.POST)
       if form.is_valid(): 
            mail = form.cleaned_data.get("email")
            contraseña = form.cleaned_data.get("password")
            user = authenticate(request, email=mail, password=contraseña)
            if user is not None:
                personal_auth_login(request, user)
                return redirect('/personal_vacunatorio/')
            else:
                messages.error(request, "Alguna/s de las credenciales ingresadas son incorrectas.")  
       else: 
             messages.error(request, "informacion")
    form = PersonalSignIn()     
    context = {'form' : form}
    return render(request, 'personalVacunatorio/login.html', context)


@login_required(login_url='/personal_vacunatorio/login_error/')
def listar_turnos(request):

    today = datetime.today().strftime('%Y-%m-%d')

    turnos = PacientesTurnos.objects.filter(fecha_confirmada = today)
    return render(request, "personalVacunatorio/listar_turnos.html/", {'turnos' : turnos})