from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm

from pacientes.models import Usuarios, VacunasAplicadas,PacientesSolicitudes
from pacientes.models import PacientesTurnos



def home_admin(request):
    return render(request, 'admin/index.html')


def ver_vacunas(request,*args,**kwargs):
    vacunas = VacunasAplicadas.objects.filter(paciente_id__user=kwargs['pk'])\
        .values('vacuna_id__nombre', 'fecha_vacunacion', 'vacuna_id')

    return render(request, "admin/listar_vacunas.html/", {'vacunas' : vacunas})


class PersonalPasswordChangeView(PasswordChangeView):
    def get_form_kwargs(self):
        personal_user = Usuarios.objects.get(id=self.kwargs['pk'])
        kwargs = super().get_form_kwargs()
        kwargs["user"] = personal_user
        return kwargs

    def form_valid(self, form):
        form.save()
        # Updating the password logs out all other sessions for the user
        # except the current one.
        update_session_auth_hash(self.request, form.user)
        
        user_email = Usuarios.objects.get(id=self.kwargs['pk']).email
        messages.success(self.request, 'La contraseña del usuario "%s" fue correctamente modificada.' % (user_email))
        return super().form_valid(form)

class PersonalChangePassword(PersonalPasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'admin/personal_password_change_form.html'
    success_url ="/admin/personalVacunatorio/usuariosadministradores/"
    
    
def admin_asignar_turno(request,**kwargs):
     if request.method == 'POST':
       solicitud = PacientesSolicitudes.objects.get(solicitud_id=kwargs['pk'])
       confirmed_date = solicitud.fecha_estimada
       turno = PacientesTurnos(
          solicitud=solicitud,
          turno_perdido    = 0,
          turno_pendiente  = 1,
          turno_completado = 0,
          fecha_confirmada = confirmed_date,
        )               
       turno.save()
       solicitud.solicitud_aprobada = 1
       solicitud.save()
       messages.success(request,"se confirmo turno el dia ",confirmed_date ,(confirmed_date))
       return redirect('/admin/pacientes/solicitudesnoriesgo/')
     return render(request, 'admin/turno_asignado.html')    