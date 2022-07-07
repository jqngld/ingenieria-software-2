from django.contrib import admin
from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import PersonalSignUpForm, PersonalChangeForm
from .models import PersonalDetalles
from pacientes.models import Usuarios


class UsuariosAdministradores(Usuarios):
    class Meta:
        proxy = True
        verbose_name_plural = 'Administradores de Vacunatorios'

@admin.register(UsuariosAdministradores)
class PersonalAdmin(admin.ModelAdmin):
    # form = PersonalSignUpForm
    # actions = ['list_admins']
    # list_display = ('email',) Continuar
    # search_fields = ('email',)


    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            # formulario para agregar un nuevo usuario personal
            kwargs['form'] = PersonalSignUpForm
            form = super().get_form(request, obj, **kwargs)
        else:
            # formulario para modificar un usuario personal
            kwargs['form'] = PersonalChangeForm
            form = super().get_form(request, obj, **kwargs)

            personal_user = PersonalDetalles.objects.get(user=obj.id)
            form.base_fields['nombre'].initial = personal_user.nombre
            form.base_fields['apellido'].initial = personal_user.apellido
            form.base_fields['numero_telefono'].initial = personal_user.numero_telefono
            form.base_fields['centro_vacunatorio'].initial = personal_user.centro_vacunatorio
            form.base_fields['fecha_nacimiento'].initial = personal_user.fecha_nacimiento.strftime('%Y-%m-%d')

        return form


    # sobreescribo el método de buscado de elementos para filtrar por criterios
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        queryset = queryset.filter(tipo_usuario='personal')

        return queryset, use_distinct


    # @admin.action(description='Listar Usuarios seleccionado/s')
    def list_admins(self, request, queryset):

        if 'apply' in request.POST:
            print('> Listar administradores vacunatorios:')
            for user in queryset:
                print(user.email)

            confirmed_date = request.POST.get('confirmed_date')
            messages.success(request, 'Se confirmó la fecha de turno %s para %s solicitudes.' % (confirmed_date, queryset.count()))

            return redirect('%s' % (request.get_full_path()))

        context = {'orders' : queryset}
        return render(request, 'admin/asignar_turno_intermedio.html', context)