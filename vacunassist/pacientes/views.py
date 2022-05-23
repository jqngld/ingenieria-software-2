from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as django_logout
from django.views import View
from django.views.generic.edit import UpdateView
from .models import *
from .forms import UserSignUpForm,UserSign,UserUpdateForm
#pdf
from django.shortcuts import (get_object_or_404,
                              render,
                              HttpResponseRedirect)
from unittest import result
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO


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
        .values('vacuna_id__nombre', 'fecha_vacunacion', 'vacuna_id')

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



# class editar_perfil(UpdateView):
    # specify the model you want to use
    model = PacientesDetalles
    form_class = UserUpdateForm()
    template_name = 'pacientes/editar_perfil.html'
    # specify the fields
    fields = [
         "sexo", "centro_vacunatorio"
        #agregar campos que especificaste en el UserUpdateForm
     ]

    success_url ="/pacientes/mi_perfil/"
    def get_object(self):
        return PacientesDetalles.objects.get(user_id=self.request.user.id)

 
# update view for details
def editar_perfil(request):
    # dictionary for initial data with
    # field names as keys
    context ={}
    id = request.user.id
    # fetch the object related to passed id
    obj = get_object_or_404(PacientesDetalles,user_id=request.user.id)
 
    # pass the object as instance in form
    form = UserUpdateForm(request.POST or None, instance = obj)
 
    # save the data from the form and
    # redirect to detail_view
    if form.is_valid():
        form.save()
        return redirect("/pacientes/mi_perfil/")
 
    # add form dictionary to context
    context["form"] = form
 
    return render(request,'pacientes/editar_perfil.html', context)        


class descargar_comprobante(View):

    def get(self, request, *args, **kwargs):

        paciente = PacientesDetalles.objects.get(user_id=request.user.id)

        solicitud = PacientesSolicitudes.objects.filter(paciente_id=paciente.paciente_id, vacuna_id=kwargs['vacuna_id'])\
            .values('centro_vacunatorio')
        vacuna = VacunasAplicadas.objects.filter(paciente_id=paciente.paciente_id, vacuna_id=kwargs['vacuna_id'])\
            .values('vacuna_id__nombre', 'fecha_vacunacion')

        fecha_descarga = datetime.today()

        context = {
            'fecha' : fecha_descarga,
            'vacuna' : vacuna[0],
            'paciente' : paciente,
            'solicitud' : solicitud[0] if solicitud else False
        }

        template = get_template('comprobante_vacunacion.html')
        html = template.render(context)

        response = HttpResponse(content_type='application/pdf')
        # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
        pisaStatus = pisa.CreatePDF(html, dest=response)

        if pisaStatus.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response
