from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate
from django.contrib.auth import logout as personal_logout
from django.contrib.auth import login as personal_auth_login
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib.auth.views import PasswordChangeView,PasswordResetView,PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.forms import PasswordChangeForm ,PasswordResetForm,SetPasswordForm
from django.urls import reverse_lazy
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
            if user is not None and user.tipo_usuario == 'personal':
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


@login_required(login_url='/personal_vacunatorio/login_error/')
def listar_historial_atendidos(request):

    today = datetime.today().strftime('%Y-%m-%d')
    centro_vacunatorio = PersonalDetalles.objects.get(user_id=request.user.id).centro_vacunatorio

    turnos = PacientesTurnos.objects.filter(
                turno_completado = 1,
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

    return render(request, "personalVacunatorio/listar_historial_atendidos.html/", {'turnos' : turnos, 'personal_centro' : centro_vacunatorio})


@login_required(login_url='/personal_vacunatorio/login_error/')
def listar_historial_ausentes(request):

    today = datetime.today().strftime('%Y-%m-%d')
    centro_vacunatorio = PersonalDetalles.objects.get(user_id=request.user.id).centro_vacunatorio

    turnos = PacientesTurnos.objects.filter(
                turno_perdido = 1,
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

    return render(request, "personalVacunatorio/listar_historial_ausentes.html/", {'turnos' : turnos, 'personal_centro' : centro_vacunatorio})


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

    if request.method == 'POST':
        form = devolucionForm(request.POST)
        if form.is_valid():
            # cambio el estado del turno a completado
            turno = PacientesTurnos.objects.get(turno_id = kwargs['turno_id'])
            turno.turno_pendiente = False
            turno.turno_completado = True
            turno.save()

            # genero la vacuna aplicada con la información detallada            
            vacuna_aplicada = VacunasAplicadas(
                vacuna_id = kwargs['vacuna_nombre'],
                paciente_id = kwargs['paciente_dni'],
                lote = form.cleaned_data.get('lote'),
                observacion = form.cleaned_data.get('observacion'),
                fecha_vacunacion = datetime.today().strftime('%Y-%m-%d'),
            )
            vacuna_aplicada.save()

            messages.success(request, "La asistencia al turno fue confirmada con éxito.")
            return redirect('/personal_vacunatorio/turnos/')
        else:
            return render(request, 'personalVacunatorio/devolucion.html', context)

    else:
        vacuna = VacunasDetalles.objects.get(nombre=kwargs['vacuna_nombre'])
        paciente = PacientesDetalles.objects.get(dni=kwargs['paciente_dni'])

        form = devolucionForm()
        context = {
            'form': form,
            'turno_id': kwargs['turno_id'],
            'vacuna_id' : vacuna.vacuna_id,
            'paciente_id' : paciente.paciente_id,
        }

    return render(request, 'personalVacunatorio/devolucion.html', context)
    

 # def vacunacion_exitosa(request, **kwargs):

#     vacuna = VacunasDetalles.objects.get(nombre=kwargs['vacuna_nombre'])
#     paciente = PacientesDetalles.objects.get(dni=kwargs['paciente_dni'])
    
#     turno = PacientesTurnos.objects.get(turno_id = kwargs['turno_id'])
#     turno.turno_pendiente = False
#     turno.turno_completado = True
#     turno.save()
    
#     vacuna_aplicada = VacunasAplicadas(
#         vacuna_id = vacuna.vacuna_id,
#         fecha_vacunacion = datetime.today().strftime('%Y-%m-%d'),
#         paciente_id = paciente.paciente_id,
#     )
#     vacuna_aplicada.save()
    
#     form = devolucionForm()  
#     context = {'vacuna_aplicada': vacuna_aplicada.id, 'form': form} 
#     return render(request, 'personalVacunatorio/devolucion.html', context)


def vacunacion_fallida(request, **kwargs): #Inasistencia

    turno = PacientesTurnos.objects.get(turno_id = kwargs['turno_id'])

    turno.turno_pendiente = False
    turno.turno_perdido = True
    turno.save()

    #Generar nueva solicitud

    messages.success(request, "La ausencia al turno fue registrada con éxito.")
    return redirect('/personal_vacunatorio/turnos/')


def marcar_inasistencias(request):

    hoy = datetime.today().strftime('%Y-%m-%d')
    centro_vacunatorio = PersonalDetalles.objects.get(user_id=request.user.id).centro_vacunatorio
    turnos = PacientesTurnos.objects.filter(fecha_confirmada = hoy, turno_pendiente = True, solicitud_id__centro_vacunatorio = centro_vacunatorio).update(turno_perdido = True, turno_pendiente = False)

    messages.success(request, "La ausencia a todos los turnos fue registrada con éxito.")
    return redirect('/personal_vacunatorio/turnos/')





class LoginAfterPasswordChangeView(PasswordChangeView):
    @property
    def success_url(self):
        return reverse_lazy('inicio_sesion/')

login_after_password_change = login_required(LoginAfterPasswordChangeView.as_view())


     
     
def restPasswordPer(request):   
    if request.method == "POST":
        form = PasswordResetForm(data=request.POST)
        if form.is_valid(): 
            mail = form.cleaned_data.get("email")
            if Usuarios.objects.filter(email=mail).exists():
                form.save(from_email='blabla@blabla.com', email_template_name='registration/password_reset_email.html', request=request)
                return redirect('/personal_vacunatorio/restablecer-contrasenia-hecho')          
            else:
                messages.error(request, " El mail ingresado no es correcto o no lo tenemos registrado en el sistema ")  
        else: 
              messages.error(request, " No existe ese mail") 
    form =  PasswordResetForm()     
    context = {'form' : form}
    return render(request, 'personalVacunatorio/restablecer-contrasenia.html', context)     
     
      
class restPasswordConfirm(PasswordResetConfirmView):
      form_class = SetPasswordForm

                
#class restPassword(PasswordResetView):
 #    form_class = PasswordResetForm
  #   success_url ="/pacientes/restablecer-contrasenia-hecho/"     

def restDone(request):
    
    return render(request, 'personalVacunatorio/restablecer-contrasenia-hecho.html')     