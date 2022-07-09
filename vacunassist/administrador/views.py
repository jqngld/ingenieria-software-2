from django.shortcuts import render
from pacientes.models import VacunasAplicadas

def home_admin(request):
    return render(request, 'admin/index.html')






def ver_vacunas(request,*args,**kwargs):
    vacunas = VacunasAplicadas.objects.filter(paciente_id__user=kwargs['pk'])\
        .values('vacuna_id__nombre', 'fecha_vacunacion', 'vacuna_id')

    return render(request, "admin/listar_vacunas.html/", {'vacunas' : vacunas})