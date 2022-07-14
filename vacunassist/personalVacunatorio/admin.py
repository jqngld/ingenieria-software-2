from django.contrib import admin
from django.contrib import messages
from django.utils.html import mark_safe
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from .forms import PersonalSignUpForm, PersonalChangeForm
from .models import PersonalDetalles
from pacientes.models import Usuarios


class UsuariosAdministradores(Usuarios):
    class Meta:
        proxy = True
        verbose_name_plural = 'Administradores de Vacunatorios'

@admin.register(UsuariosAdministradores)
class PersonalAdmin(admin.ModelAdmin):

    actions = ['delete_multiple_users']
    list_display = ('nombre', 'apellido', 'email', 'centro_vacunatorio', 'boton')
    search_fields = ('personaldetalles__nombre', 'personaldetalles__apellido', 'email', 'personaldetalles__centro_vacunatorio')
    list_display_links = None


    @admin.display(description='Acciones')
    def boton(self, obj):
        # el parámetro 'obj.pk' es el id del objeto dentro de la línea, hay que pasarlo en
        # el link para saber qué objeto se va a usar, estos botones son de ejemplo y hacen lo mismo

        render_action_buttons = render_to_string('admin/personal_action_buttons.html', {'pk' : obj.pk})
        return mark_safe(render_action_buttons)

    @admin.display(description='Nombre')
    def nombre(self, obj):
        return obj.personaldetalles.nombre

    @admin.display(description='Apellido')
    def apellido(self, obj):
        return obj.personaldetalles.apellido

    @admin.display(description='Número Teléfono')
    def numero_telefono(self, obj):
        return obj.personaldetalles.numero_telefono

    @admin.display(description='Fecha Nacimiento')
    def fecha_nacimiento(self, obj):
        return obj.personaldetalles.fecha_nacimiento

    @admin.display(description='Centro Vacunatorio')
    def centro_vacunatorio(self, obj):
        return obj.personaldetalles.centro_vacunatorio


    # función para no permitir que se elimine un elemento
    def has_delete_permission(self, request, obj=None):
        return False

    def get_fields(self, request, obj=None):
        if obj is None:
            fields = (('nombre', 'apellido',), ('email', 'numero_telefono'), 'fecha_nacimiento', 'centro_vacunatorio', ('password1', 'password2'))
        else:
            fields = (('nombre', 'apellido',), ('email', 'numero_telefono'), 'fecha_nacimiento', 'centro_vacunatorio')
        return fields

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
        queryset = queryset.filter(tipo_usuario='personal').select_related('personaldetalles')

        return queryset, use_distinct


    @admin.action(description='Eliminar usuarios seleccionados')
    def delete_multiple_users(self, request, queryset):

        if 'apply' in request.POST:
            for user in queryset:
                user.delete()
            messages.success(request, 'Se eliminaron correctamente %s usuarios administradores de vacunatorios.' % (queryset.count()))
            return redirect('%s' % (request.get_full_path()))

        context = {'orders' : queryset}
        return render(request, 'admin/personal_multiple_delete.html', context)