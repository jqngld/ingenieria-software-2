from django.shortcuts import render
from pacientes.models import *

from datetime import datetime 


def home(request):
    return render(request, 'personalVacunatorio/index.html')


def login(request):
    pass


def listar_turnos(request):

    today = datetime.today().strftime('%Y-%m-%d')

    turnos = PacientesTurnos.objects.filter(fecha_confirmada = today)#\
        # .values('solicitud_id__paciente_id', 'fecha_confirmada')
    return render(request, "personalVacunatorio/listar_turnos.html/", {'turnos' : turnos})