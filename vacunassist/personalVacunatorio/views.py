from optparse import Values
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate
from django.contrib.auth import logout as personal_logout
from django.contrib.auth import login as personal_auth_login
from django.contrib.auth.decorators import login_required
from django.views import View

from pacientes.models import *
from .forms import *

from datetime import datetime 
from dateutil.relativedelta import relativedelta

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

    today = '2022-06-12' #datetime.today().strftime('%Y-%m-%d')

    turnos = PacientesTurnos.objects.filter(fecha_confirmada = today)\
                .values('solicitud_id__paciente_id__nombre',
                        'solicitud_id__paciente_id__apellido',
                        'solicitud_id__paciente_id__dni',
                        'solicitud_id__paciente_id__fecha_nacimiento',
                        'solicitud_id__vacuna_id__nombre')
    
    for turno in turnos:
        turno['paciente_nombre']    = turno['solicitud_id__paciente_id__nombre']
        turno['paciente_apellido']  = turno['solicitud_id__paciente_id__apellido']
        turno['paciente_dni']       = turno['solicitud_id__paciente_id__dni']
        turno['vacuna_nombre']      = turno['solicitud_id__vacuna_id__nombre']

        del turno['solicitud_id__paciente_id__nombre']
        del turno['solicitud_id__paciente_id__apellido']
        del turno['solicitud_id__paciente_id__dni']
        del turno['solicitud_id__vacuna_id__nombre']

        fecha_nacimiento = turno['solicitud_id__paciente_id__fecha_nacimiento']
        del turno['solicitud_id__paciente_id__fecha_nacimiento']
        edad = relativedelta(datetime.now(), fecha_nacimiento)
        turno['paciente_edad'] = edad.years

    return render(request, "personalVacunatorio/listar_turnos.html/", {'turnos' : turnos})




def devolucion(request):
    if request.method == 'POST':
        form = devolucionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/personal_vacunatorio/')  
    form = devolucionForm()  
    context = {'form': form}
    return render(request, 'personalVacunatorio/devolucion.html/', context) 

      