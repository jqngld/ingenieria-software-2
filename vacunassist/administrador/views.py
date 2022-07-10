from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from administrador.forms import SalesSearchForm

from pacientes.models import Usuarios, VacunasAplicadas,PacientesSolicitudes
from pacientes.models import PacientesTurnos

from .utils import get_chart
from pacientes.models import PacientesSolicitudes, Usuarios, VacunasAplicadas

import pandas
pandas.set_option('display.max_columns', None)  


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

def personal_detele_user(request, *args, **kwargs):

    personal_user = Usuarios.objects.get(id=kwargs['pk'])
    messages.success(request, 'El usuario "%s" fue eliminado correctamente.' % (personal_user.email))

    personal_user.delete()
    return redirect('/admin/personalVacunatorio/usuariosadministradores/')


def search_dates(request):

    df_solicitudes = None

    chart = None
    no_data = None
    search_form = SalesSearchForm(request.POST or None)

    if request.method == 'POST':
        date_to = request.POST.get('date_to')
        date_from = request.POST.get('date_from')
        chart_type = request.POST.get('chart_type')
        results_by = request.POST.get('results_by')
        print(date_from, date_to, chart_type)

        solicitudes = PacientesSolicitudes.objects.filter(fecha_estimada__lte=date_to, fecha_estimada__gte=date_from)

        if len(solicitudes) > 0:
            df_solicitudes = pandas.DataFrame(solicitudes.values())

            # sales_df['fecha_estimada'] = sales_df['fecha_estimada']
            # sales_df.rename({'customer_id': 'customer', 'salesman_id': 'salesman', 'id': 'sales_id'}, axis=1,
            #                 inplace=True)

            chart = get_chart(chart_type, df_solicitudes, results_by)
            df_solicitudes = df_solicitudes.to_html()

        else:
            messages.warning(request, 'No se encontró información para los filtros seleccionados.')

    context = {
        'chart': chart,
        'sales_df': df_solicitudes,
        'search_form': search_form,
    }
    return render(request, 'admin/search_dates.html', context)
