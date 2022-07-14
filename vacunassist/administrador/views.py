from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from administrador.forms import SalesSearchForm

from pacientes.models import PacientesDetalles, Usuarios, VacunasAplicadas,PacientesSolicitudes
from pacientes.models import PacientesTurnos

from .utils import get_chart_solicitud, get_chart_turnos
from pacientes.models import PacientesSolicitudes, Usuarios, VacunasAplicadas

import pandas
pandas.set_option('display.max_columns', None)  


def home_admin(request):
    return render(request, 'admin/index.html')


def ver_vacunas(request,*args,**kwargs):
    paciente = PacientesDetalles.objects.get(user=kwargs['pk'])
    vacunas = VacunasAplicadas.objects.filter(paciente_id__user=kwargs['pk'])\
        .values('vacuna_id__nombre', 'fecha_vacunacion', 'vacuna_id')

    context = {
        'vacunas' : vacunas,
        'paciente_nombre' : paciente.nombre,
        'paciente_apellido' : paciente.apellido,
    }
    return render(request, "admin/listar_vacunas.html/", context)


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
    messages.success(request,'se confirmo turno el dia %s' % (confirmed_date))
    if not (solicitud.paciente.es_paciente_riesgo):
      return redirect('/admin/pacientes/solicitudesnoriesgo/')   
    else:
      return redirect('/admin/pacientes/solicitudesriesgo/')

def paciente_detele_user(request, *args, **kwargs):

    patient_user = Usuarios.objects.get(id=kwargs['pk'])
    messages.success(request, 'El usuario "%s" fue eliminado correctamente.' % (patient_user.email))

    patient_user.delete()
    return redirect('/admin/pacientes/usuariospacientes/')


def personal_detele_user(request, *args, **kwargs):

    personal_user = Usuarios.objects.get(id=kwargs['pk'])
    messages.success(request, 'El usuario "%s" fue eliminado correctamente.' % (personal_user.email))

    personal_user.delete()
    return redirect('/admin/personalVacunatorio/usuariosadministradores/')


def search_dates(request):

    df_turnos = None
    df_solicitudes = None

    chart_turnos_1 = None
    chart_turnos_2 = None
    chart_turnos_3 = None

    chart_solicitudes_1 = None
    chart_solicitudes_2 = None
    chart_solicitudes_3 = None

    search_form = SalesSearchForm(request.POST or None)

    if request.method == 'POST':
        # agregar filtro para pacientes de riesgo
        date_to = request.POST.get('date_to')
        date_from = request.POST.get('date_from')

        turnos = PacientesTurnos.objects.filter(fecha_confirmada__lte=date_to, fecha_confirmada__gte=date_from, turno_pendiente=1)
        solicitudes = PacientesSolicitudes.objects.filter(fecha_estimada__lte=date_to, fecha_estimada__gte=date_from)

        if len(solicitudes) > 0:
            df_solicitudes = pandas.DataFrame(solicitudes.values())

            df_turnos = pandas.DataFrame(turnos.values())\
                            .merge(df_solicitudes, on='solicitud_id', how='left')

            df_solicitudes = pandas.DataFrame(solicitudes.filter(solicitud_aprobada=0).values())
            

            # sales_df['fecha_estimada'] = sales_df['fecha_estimada']
            # sales_df.rename({'customer_id': 'customer', 'salesman_id': 'salesman', 'id': 'sales_id'}, axis=1,
            #                 inplace=True)

            chart_solicitudes_1 = get_chart_solicitud(df_solicitudes, 'Terminal')
            chart_solicitudes_2 = get_chart_solicitud(df_solicitudes, 'Cementerio')
            chart_solicitudes_3 = get_chart_solicitud(df_solicitudes, 'Municipalidad')

            chart_turnos_1 = get_chart_turnos(df_turnos, 'Terminal')
            chart_turnos_2 = get_chart_turnos(df_turnos, 'Cementerio')
            chart_turnos_3 = get_chart_turnos(df_turnos, 'Municipalidad')

            df_turnos = df_turnos.to_html()
            df_solicitudes = df_solicitudes.to_html()

        else:
            messages.warning(request, 'No se encontró información para los filtros seleccionados.')

    context = {
        'turnos': df_turnos,
        'solicitudes': df_solicitudes,
        'search_form': search_form,
        'chart_turnos_1' : chart_turnos_1,
        'chart_turnos_2' : chart_turnos_2,
        'chart_turnos_3' : chart_turnos_3,
        'chart_solicitudes_1' : chart_solicitudes_1,
        'chart_solicitudes_2' : chart_solicitudes_2,
        'chart_solicitudes_3' : chart_solicitudes_3,
    }
    return render(request, 'admin/search_dates.html', context)
