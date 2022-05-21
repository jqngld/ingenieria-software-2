from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as django_logout
from .models import *
from .forms import UserSignUpForm,UserSign


def home(request):
    return render(request, 'pacientes/index.html')


def login_error(request):
    return HttpResponse('Usuario no logueado.')


@login_required(login_url='/pacientes/login_error/')
def inicio_pacientes(request):
    return HttpResponse('Página inicio de pacientes.')


def login(request):   
    if request.method == "POST":
       form = UserSign(data=request.POST)
       if form.is_valid(): 
            mail = form.cleaned_data.get("email")
            contraseña = form.cleaned_data.get("password")
            token = form.cleaned_data.get("token")
            user = authenticate(request, email=mail, password=contraseña)
            if user is not None and PacientesDetalles.objects.filter(token=token,user=user).exists():
                auth_login(request, user)
                return redirect('/pacientes/')
            else:
                 messages.error(request, "usuario no valido")  
       else: 
             messages.error(request, "informacion")                     
    form = UserSign()     
    context = {'form' : form}
    return render(request, 'pacientes/login.html', context)


def logout(request):
    
    django_logout(request)
    return redirect('/pacientes/')


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


def view_profile(request):
    paciente = PacientesDetalles.objects.get(user_id=request.user.id)
    return render(request, "pacientes/view_profile.html/", {"datos": paciente})


def listar_vacunas(request):
    paciente = PacientesDetalles.objects.get(user_id=request.user.id)

    vacunas = VacunasAplicadas.objects.filter(paciente_id=paciente.paciente_id)\
        .values('vacuna_id__nombre', 'fecha_vacunacion')

    return render(request, "pacientes/listar_vacunas.html/", {'vacunas' : vacunas})

def listar_solicitudes(request):
    paciente = PacientesDetalles.objects.get(user_id=request.user.id)

    solicitudes = PacientesSolicitudes.objects.filter(paciente_id=paciente.paciente_id)\
        .values('vacuna_id__nombre', 'fecha_solicitud', 'solicitud_aprobada')
    return render(request, "pacientes/listar_solicitudes.html/", {'solicitudes' : solicitudes})

def listar_turnos(request):
    paciente = PacientesDetalles.objects.get(user_id=request.user.id)

    turnos = PacientesTurnos.objects.filter(
        solicitud_id__paciente_id=paciente.paciente_id,
        solicitud_id__solicitud_aprobada=True)\
            .values('solicitud_id__vacuna_id__nombre', 'fecha_confirmada', 'turno_perdido', 'turno_pendiente', 'turno_completado')
    return render(request, "pacientes/listar_turnos.html/", {'turnos' : turnos})






