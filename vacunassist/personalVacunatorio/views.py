from multiprocessing import context
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
def listar_turnos_diarios(request):

    today = datetime.today().strftime('%Y-%m-%d')
    centro_vacunatorio = PersonalDetalles.objects.get(user_id=request.user.id).centro_vacunatorio

    turnos = PacientesTurnos.objects.filter(
                turno_pendiente = 1,
                fecha_confirmada=today,
                solicitud_id__centro_vacunatorio=centro_vacunatorio)\
                    .values('turno_id',
                        'solicitud_id__vacuna_id__nombre',
                        'solicitud_id__paciente_id__dni',
                        'solicitud_id__paciente_id__sexo',
                        'solicitud_id__paciente_id__nombre',
                        'solicitud_id__paciente_id__apellido',
                        'solicitud_id__paciente_id__fecha_nacimiento',
                        'solicitud_id__paciente_id__es_paciente_riesgo',
                        'solicitud_id__paciente_id__centro_vacunatorio')

    for turno in turnos:
        turno['vacuna_nombre']      = turno['solicitud_id__vacuna_id__nombre']
        turno['paciente_dni']       = turno['solicitud_id__paciente_id__dni']
        turno['paciente_sexo']      = turno['solicitud_id__paciente_id__sexo']
        turno['paciente_nombre']    = turno['solicitud_id__paciente_id__nombre']
        turno['paciente_apellido']  = turno['solicitud_id__paciente_id__apellido']
        turno['paciente_centro']    = turno['solicitud_id__paciente_id__centro_vacunatorio']
        turno['paciente_riesgo']    = turno['solicitud_id__paciente_id__es_paciente_riesgo']
        fecha_nacimiento            = turno['solicitud_id__paciente_id__fecha_nacimiento']
        turno['paciente_fecha_nac'] = turno['solicitud_id__paciente_id__fecha_nacimiento'].strftime('%d-%m-%Y')

        del turno['solicitud_id__vacuna_id__nombre']
        del turno['solicitud_id__paciente_id__dni']
        del turno['solicitud_id__paciente_id__sexo']
        del turno['solicitud_id__paciente_id__nombre']
        del turno['solicitud_id__paciente_id__apellido']
        del turno['solicitud_id__paciente_id__fecha_nacimiento']
        del turno['solicitud_id__paciente_id__centro_vacunatorio']
        del turno['solicitud_id__paciente_id__es_paciente_riesgo']

        edad = relativedelta(datetime.now(), fecha_nacimiento)
        turno['paciente_edad'] = edad.years

    return render(request, "personalVacunatorio/listar_turnos.html/", {'turnos' : turnos, 'personal_centro' : centro_vacunatorio})





def devolucion(request, **kwargs):

    vacuna_id = kwargs['vacuna_aplicada']
    vacuna = VacunasAplicadas.objects.get(id = vacuna_id)
    if request.method == 'POST':
        form = devolucionForm(request.POST)
        if form.is_valid():
            vacuna.lote = form.cleaned_data.get("lote")
            vacuna.observacion = form.cleaned_data.get("observacion")
            vacuna.save()
            return redirect('/personal_vacunatorio/turnos')  
    form = devolucionForm()  
    context = {'form': form}
    return render(request, 'personalVacunatorio/devolucion.html', context) 

    

def vacunacion_exitosa(request, **kwargs):

    paciente = PacientesDetalles.objects.get(dni=kwargs['paciente_dni'])
    vacuna = VacunasDetalles.objects.get(nombre=kwargs['vacuna_nombre'])
    turno_completado = PacientesTurnos(
            turno_id = kwargs['turno_id'],
            solicitud_id = kwargs['turno_id'],
            turno_pendiente = False,
            turno_completado = True,
        )
    turno_completado.save()
    vacuna_aplicada = VacunasAplicadas(
        vacuna_id = vacuna.vacuna_id,
        fecha_vacunacion = datetime.today().strftime('%Y-%m-%d'),
        paciente_id = paciente.paciente_id,
    )
    vacuna_aplicada.save()
    form = devolucionForm()  
    context = {'vacuna_aplicada': vacuna_aplicada.id, 'form': form} 
    return render(request, 'personalVacunatorio/devolucion.html', context)


def vacunacion_fallida(request, **kwargs): #Inasistencia

    turno = PacientesTurnos.objects.filter(turno_id=kwargs['turno_id'])
    inasistencia = PacientesTurnos(
            turno_id = kwargs['turno_id'],
            solicitud_id = kwargs['turno_id'],
            turno_perdido = True,
            turno_pendiente = False,
        )
    inasistencia.save()
    #Generar nueva solicitud
    return redirect('/personal_vacunatorio/turnos/')
