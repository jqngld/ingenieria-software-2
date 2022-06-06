from django.contrib import messages
from django.shortcuts import redirect, render
from pacientes.models import *
from django.contrib.auth import authenticate
from .forms import *
from django.contrib.auth import login as auth_login

from datetime import datetime 


def home_personal(request):
    return render(request, 'personalVacunatorio/index.html')



def listar_turnos(request):

    today = datetime.today().strftime('%Y-%m-%d')

    turnos = PacientesTurnos.objects.filter(fecha_confirmada = today)#\
        # .values('solicitud_id__paciente_id', 'fecha_confirmada')
    return render(request, "personalVacunatorio/listar_turnos.html/", {'turnos' : turnos})

def login_personal(request):   
    if request.method == "POST":
       form = UserSign(data=request.POST)
       if form.is_valid(): 
            mail = form.cleaned_data.get("email")
            contraseña = form.cleaned_data.get("password")
            user = authenticate(request, email=mail, password=contraseña)
            if user is not None:
                auth_login(request, user)
                return redirect('/personal_vacunatorio/turnos')
            else:
                 messages.error(request, "Alguna/s de las credenciales ingresadas son incorrectas.")  
    form = UserSign()     
    context = {'form' : form}
    return render(request, 'personalVacunatorio/login.html', context)