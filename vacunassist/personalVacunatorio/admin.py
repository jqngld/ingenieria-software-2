from django.contrib import admin
from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import PersonalSignUpForm
from .models import PersonalDetalles
from pacientes.models import Usuarios

from datetime import datetime


class UsuariosAdministradores(Usuarios):
    class Meta:
        proxy = True
        verbose_name_plural = 'Administradores de Vacunatorios'

@admin.register(UsuariosAdministradores)
class PersonalAdmin(admin.ModelAdmin):
    form = PersonalSignUpForm
    actions = ['list_admins']

    fields = ('nombre', 'apellido', 'numero_telefono', 'fecha_nacimiento', 'email', 'centro_vacunatorio', 'password1', 'password2')


    # def get_list_display_links(self, request, list_display):
    #     """
    #     Return a sequence containing the fields to be displayed as links
    #     on the changelist. The list_display parameter is the list of fields
    #     returned by get_list_display().

    #     We override Django's default implementation to specify no links unless
    #     these are explicitly set.
    #     """
    #     if self.list_display_links or not list_display:
    #         return self.list_display_links
    #     else:
    #         return (None,)

    def get_form(self, request, obj=None, **kwargs):
        form = super(PersonalAdmin, self).get_form(request, obj, **kwargs)

        user = PersonalDetalles.objects.get(user=obj.id)

        print(obj.password)
        form.base_fields['password1'].widget.render_value = True
        form.base_fields['password2'].widget.render_value = True
        form.base_fields['password1'].initial = obj.password
        form.base_fields['password2'].initial = obj.password
        
        form.base_fields['nombre'].initial = user.nombre
        form.base_fields['apellido'].initial = user.apellido
        form.base_fields['numero_telefono'].initial = user.numero_telefono
        form.base_fields['fecha_nacimiento'].initial = user.fecha_nacimiento.strftime('%Y-%m-%d')

        return form

    # sobreescribo el método de buscado de elementos para filtrar por criterios
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        queryset = queryset.filter(tipo_usuario='personal')

        return queryset, use_distinct

    @admin.action(description='Listar Usuarios seleccionado/s')
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