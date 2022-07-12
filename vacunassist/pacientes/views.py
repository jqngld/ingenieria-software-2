import email
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as django_logout
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.views import PasswordChangeView,PasswordResetView,PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.forms import PasswordChangeForm ,PasswordResetForm,SetPasswordForm
from .models import *
from .forms import *
from django.shortcuts import HttpResponseRedirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from xhtml2pdf import pisa
from dateutil.relativedelta import relativedelta


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
                messages.error(request, "Alguna/s de las credenciales ingresadas son incorrectas.")  
        else: 
            messages.error(request, "informacion")
    form = UserSign()     
    context = {'form' : form}
    return render(request, 'pacientes/login.html', context)


def logout(request):
    
    django_logout(request)
    return redirect('/pacientes/')


def signup1(request):

    if request.method == 'POST':
        form = UserSignUp1Form(request.POST)
        if form.is_valid():
            form_usuario = UserSignUpForm(initial={
            'password2': form.cleaned_data.get("password2"),
            'password1': form.cleaned_data.get("password1")})

            form_usuario.fields['nombre'].initial = form.cleaned_data.get("nombre")
            form_usuario.fields['apellido'].initial = form.cleaned_data.get("apellido")
            form_usuario.fields['email'].initial = form.cleaned_data.get("email")
            form_usuario.fields['password1'].widget.render_value = True
            form_usuario.fields['password2'].widget.render_value = True
            context = {'form' : form_usuario}
            return render(request, 'pacientes/signup2.html', context)
    else:
        form = UserSignUp1Form()

    context = {'form' : form}
    return render(request, 'pacientes/signup1.html', context)
    
def signup2(request):

    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/pacientes/')
        else:
            context = {'form': form}
            return render(request, 'pacientes/signup2.html', context)


@login_required(login_url='/pacientes/login_error/')
def view_profile(request):
    paciente = PacientesDetalles.objects.get(user_id=request.user.id)
    return render(request, "pacientes/view_profile.html/", {"datos": paciente})


@login_required(login_url='/pacientes/login_error/')
def listar_vacunas(request):
    paciente = PacientesDetalles.objects.get(user_id=request.user.id)

    vacunas = VacunasAplicadas.objects.filter(paciente_id=paciente.paciente_id)\
        .values('vacuna_id__nombre', 'fecha_vacunacion', 'vacuna_id')

    return render(request, "pacientes/listar_vacunas.html/", {'vacunas' : vacunas})


@login_required(login_url='/pacientes/login_error/')
def listar_solicitudes(request):
    paciente = PacientesDetalles.objects.get(user_id=request.user.id)

    solicitudes = PacientesSolicitudes.objects.filter(paciente_id=paciente.paciente_id)\
        .values('vacuna_id__nombre', 'fecha_solicitud', 'solicitud_aprobada')
    return render(request, "pacientes/listar_solicitudes.html/", {'solicitudes' : solicitudes})


@login_required(login_url='/pacientes/login_error/')
def listar_turnos(request):
    paciente = PacientesDetalles.objects.get(user_id=request.user.id)

    turnos = PacientesTurnos.objects.filter(
        solicitud_id__paciente_id=paciente.paciente_id,
        solicitud_id__solicitud_aprobada=True)\
            .values('solicitud_id__vacuna_id__nombre', 'fecha_confirmada', 'turno_perdido', 'turno_pendiente', 'turno_completado')
    return render(request, "pacientes/listar_turnos.html/", {'turnos' : turnos})


@login_required(login_url='/pacientes/login_error/')
def solicitud_fiebre_amarilla(request):

    paciente = PacientesDetalles.objects.get(user_id=request.user.id)
    
    try:
        solicitud = PacientesSolicitudes.objects.get(paciente_id=paciente.paciente_id, vacuna_id=4)
    except:
        pass

    paciente_edad = relativedelta(datetime.now(), paciente.fecha_nacimiento)

    vacuna_aplicada = VacunasAplicadas.objects.filter(paciente_id=paciente.paciente_id, vacuna_id=4).exists()
    solicitud_existente = PacientesSolicitudes.objects.filter(paciente_id=paciente.paciente_id, vacuna_id=4).exists()

    if paciente_edad.years < 60 and not vacuna_aplicada and not solicitud_existente:        
        solicitud_fa = PacientesSolicitudes(
            paciente_id = paciente.paciente_id,
            vacuna_id = 4,
            solicitud_aprobada = 0,
            fecha_estimada = datetime.today(),
            centro_vacunatorio = paciente.centro_vacunatorio
        )
        solicitud_fa.save()
        messages.success(request, "La solicitud se ha realizado de forma exitosa.")
    
    else:
        if vacuna_aplicada:
            messages.error(request, "Usted ya se ha aplicado la vacuna contra la fiebre amarilla.")
        elif paciente_edad.years >= 60:
            messages.error(request, "La vacuna contra la fiebre amarilla solo se aplica a menores de 60 años.")
        elif solicitud_existente:
            if solicitud.solicitud_aprobada:
                messages.error(request, "Usted ya recibió un turno para aplicarse esta vacuna.")
            else:
                messages.error(request, "Usted ya ha solicitado un turno para aplicarse esta vacuna.")

    return redirect('/pacientes/mis_solicitudes/')

   
class cambiarPassword(PasswordChangeView):
      form_class = PasswordChangeForm
      success_url ="/pacientes/mi_perfil/"

 
@login_required(login_url='/pacientes/login_error/')
def editar_perfil(request):
    # dictionary for initial data with
    # field names as keys
    context ={}
 
    user = request.user.id

    perfil = PacientesDetalles.objects.get(user_id=request.user.id) 

 
    # pass the object as instance in form
    form = UserUpdateForm(request.POST or None , request.FILES , instance = perfil)


    # save the data from the form and
    # redirect to detail_view
    if form.is_valid():

        perfil.sexo = form.cleaned_data.get('sexo')
        perfil.centro_vacunatorio = form.cleaned_data.get('centro_vacunatorio')
        perfil.save()
        return HttpResponseRedirect("/pacientes/mi_perfil/")
 
    # add form dictionary to context
    context["form"] = form
 
    return render(request,'pacientes/editar_perfil.html', context)        


class descargar_comprobante(View):
    def get(self, request, *args, **kwargs):

        paciente = PacientesDetalles.objects.get(user_id=request.user.id)

        solicitud = PacientesSolicitudes.objects.filter(paciente_id=paciente.paciente_id, vacuna_id=kwargs['vacuna_id'])\
            .values('centro_vacunatorio')
        vacuna = VacunasAplicadas.objects.filter(paciente_id=paciente.paciente_id, vacuna_id=kwargs['vacuna_id'])\
            .values('vacuna_id__nombre', 'fecha_vacunacion', 'lote', 'observacion')

        fecha_descarga = datetime.today()

        context = {
            'fecha' : fecha_descarga,
            'vacuna' : vacuna[0],
            'paciente' : paciente,
            'solicitud' : solicitud[0] if solicitud else False
        }

        template = get_template('pacientes/comprobante_vacunacion.html')
        html = template.render(context)

        response = HttpResponse(content_type='application/pdf')
        # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
        pisaStatus = pisa.CreatePDF(html, dest=response)

        if pisaStatus.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response


class LoginAfterPasswordChangeView(PasswordChangeView):
    @property
    def success_url(self):
        return reverse_lazy('inicio_sesion/')

login_after_password_change = login_required(LoginAfterPasswordChangeView.as_view())


     
     
def restPassword(request):   
    if request.method == "POST":
        form = PasswordResetForm(data=request.POST)
        if form.is_valid(): 
            mail = form.cleaned_data.get("email")
            if Usuarios.objects.filter(email=mail).exists():
                form.save(from_email='blabla@blabla.com', email_template_name='registration/password_reset_email.html', request=request)
                return redirect('/pacientes/restablecer-contrasenia-hecho')          
            else:
                messages.error(request, " El mail ingresado no se encuentra registrado en el sistema ")  
        else: 
              messages.error(request, " No existe ese mail") 
    form =  PasswordResetForm()     
    context = {'form' : form}
    return render(request, 'pacientes/restablecer-contrasenia.html', context)     
     
      
class restPasswordConfirm(PasswordResetConfirmView):
      form_class = SetPasswordForm

                
#class restPassword(PasswordResetView):
 #    form_class = PasswordResetForm
  #   success_url ="/pacientes/restablecer-contrasenia-hecho/"     

def restDone(request):
    
    return render(request, 'pacientes/restablecer-contrasenia-hecho.html')     
      
      
      