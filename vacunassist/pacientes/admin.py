from django.contrib import admin
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.html import mark_safe
from django.template.loader import render_to_string
from pandas import describe_option

from .models import *

from datetime import date
from dateutil.relativedelta import relativedelta


class VacunaAdmin(admin.ModelAdmin):      
    fields = ('vacuna','lote','paciente')
    list_filter = ('fecha_vacunacion',)
    list_display = ('vacuna','lote','observacion','nombrePaciente','apellido','fecha_vacunacion')  
    search_fields = ('paciente__nombre','paciente__apellido','vacuna__nombre','lote', 'fecha_vacunacion') 
    list_display_links = None

    # sobreescribo el método de buscado de elementos para filtrar por criterios
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        queryset = queryset.select_related("paciente")
        return queryset, use_distinct
      
    def nombrePaciente(self,obj):
        return obj.paciente.nombre
    nombrePaciente.short_description = 'nombre'
          
    def apellido(self,obj):
        return obj.paciente.apellido
         
         # función para no permitir que se añada un elemento
    def has_add_permission(self, request):
         return False

    # función para no permitir que se modifique un elemento
    def has_change_permission(self, request, obj=None):
        return False

    # función para no permitir que se elimine un elemento
    def has_delete_permission(self, request, obj=None):
        return False
 

class UsuariosPacientes(Usuarios):
    class Meta:
        proxy = True
        verbose_name_plural = 'Pacientes'

@admin.register(UsuariosPacientes)
class PacienteAdmin(admin.ModelAdmin):
    
    actions = ['delete_multiple_users']
    list_display = ('format_nombre','format_apellido','format_dni','format_fecha_nacimiento','email','format_centro_vacunatorio','boton')
    fields = ('format_nombre','format_apellido','format_dni','edad','email','format_centro_vacunatorio','format_sexo','format_riesgo')
    search_fields = ('email','pacientesdetalles__nombre','pacientesdetalles__apellido','pacientesdetalles__dni', 'pacientesdetalles__centro_vacunatorio','pacientesdetalles__fecha_nacimiento')
    list_display_links = None


    @admin.action(description='Eliminar usuarios seleccionados')
    def delete_multiple_users(self, request, queryset):

        if 'apply' in request.POST:
            for user in queryset:
                user.delete()
            messages.success(request, 'Se eliminaron correctamente %s usuarios pacientes.' % (queryset.count()))
            return redirect('%s' % (request.get_full_path()))

        context = {'orders' : queryset}
        return render(request, 'admin/personal_multiple_delete.html', context)


    # función para no permitir que se añada un elemento
    def has_add_permission(self, request):
        return False

    # función para no permitir que se modifique un elemento
    def has_change_permission(self, request, obj=None):
        return False

    # función para no permitir que se elimine un elemento
    def has_delete_permission(self, request, obj=None):
        return False

    # sobreescribo el método de buscado de elementos para filtrar por criterios
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        queryset = queryset.filter(tipo_usuario='paciente').select_related("pacientesdetalles")
        return queryset, use_distinct


    @admin.display(description='Acciones')
    def boton(self, obj):
        # el parámetro 'obj.pk' es el id del objeto dentro de la línea, hay que pasarlo en
        # el link para saber qué objeto se va a usar, estos botones son de ejemplo y hacen lo mismo

        render_action_buttons = render_to_string('admin/paciente_action_buttons.html', {'pk' : obj.pk})
        return mark_safe(render_action_buttons)

    @admin.display(description='Nombre')
    def format_nombre(self, obj):
        return obj.pacientesdetalles.nombre

    @admin.display(description='Apellido')
    def format_apellido(self, obj):
        return obj.pacientesdetalles.apellido
    
    @admin.display(description='sexo')
    def format_sexo(self, obj):
        return obj.pacientesdetalles.sexo

    @admin.display(description='Nacimiento')
    def format_fecha_nacimiento(self, obj):
        return obj.pacientesdetalles.fecha_nacimiento
    
    @admin.display(description='riesgo')
    def format_riesgo(self, obj):
        if obj.pacientesdetalles.es_paciente_riesgo:
            return "Si"
        else: 
            return "No"
 
    @admin.display(description='Edad')
    def edad(self, obj):
        return relativedelta(date.today(), obj.pacientesdetalles.fecha_nacimiento).years

    @admin.display(description='Dni')
    def format_dni(self, obj):
        return obj.pacientesdetalles.dni

    @admin.display(description='Centro')
    def format_centro_vacunatorio(self, obj):
        return obj.pacientesdetalles.centro_vacunatorio


class SolicitudesNoRiesgo(PacientesSolicitudes):
    class Meta:
        proxy = True
        verbose_name = 'solicitudes de pacientes'
        verbose_name_plural = 'Solicitudes de Pacientes'

@admin.register(SolicitudesNoRiesgo)
class SolicitudesNoRiesgoAdmin(admin.ModelAdmin):

    actions = ['asignar_turno']
    fields = ('paciente', 'vacuna', 'centro_vacunatorio', 'format_fecha_solicitud', 'format_fecha_estimada')
    search_fields = ('paciente__nombre', 'paciente__apellido', 'centro_vacunatorio','vacuna__nombre')
    list_display = ('nombre','apellido', 'centro_vacunatorio', 'vacuna', 'format_fecha_solicitud', 'format_fecha_estimada','boton')
    readonly_fields = ('paciente', 'vacuna', 'centro_vacunatorio', 'format_fecha_solicitud', 'format_fecha_estimada')
    list_display_links = None
    ordering = ['solicitud_id']


    @admin.display(description='Acciones')
    def boton(self, obj):
        # el parámetro 'obj.pk' es el id del objeto dentro de la línea, hay que pasarlo en
        # el link para saber qué objeto se va a usar, estos botones son de ejemplo y hacen lo mismo

        render_action_buttons = render_to_string('admin/pacientes_actions_buttons.html', {'pk' : obj.pk})
        return mark_safe(render_action_buttons)
  
  
    # función para no permitir que se añada un elemento
    def has_add_permission(self, request):
        return False

    # función para no permitir que se elimine un elemento
    def has_delete_permission(self, request, obj=None):
        return False

    # sobreescribo el método de buscado de elementos para filtrar por criterios
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        queryset = queryset.select_related('paciente').filter(solicitud_aprobada=0, paciente__es_paciente_riesgo=0)

        return queryset, use_distinct


    # aplico formatos a las fechas que se listan
    @admin.display(description='Fecha Solicitud')
    def format_fecha_solicitud(self, obj):
        return obj.fecha_solicitud.strftime('%d-%m-%Y')

    @admin.display(description='Fecha Sugerida')
    def format_fecha_estimada(self, obj):
        return obj.fecha_estimada.strftime('%d-%m-%Y')   
    
    @admin.display(description='Nombre')
    def nombre(self,obj):
        return obj.paciente.nombre
     
    @admin.display(description='Apellido')
    def apellido(self,obj):
        return obj.paciente.apellido

    # registro la acción para asignar fechas a las solicitudes
    @admin.action(description='Asignar fecha a solicitudes seleccionadas')
    def asignar_turno(self, request, queryset):

        if 'apply' in request.POST:
            confirmed_date = request.POST.get('confirmed_date')
            for solicitud in queryset:
                turno = PacientesTurnos(
                    solicitud        = solicitud,
                    turno_perdido    = 0,
                    turno_pendiente  = 1,
                    turno_completado = 0,
                    fecha_confirmada = confirmed_date,
                )
                turno.save()
                solicitud.solicitud_aprobada = 1
                solicitud.save()
            messages.success(request, 'Se confirmó la fecha de turno %s para %s solicitudes.' % (confirmed_date, queryset.count()))
            return redirect('%s' % (request.get_full_path()))

        context = {'orders' : queryset}
        return render(request, 'admin/asignar_turno_intermedio.html', context)


class SolicitudesRiesgo(PacientesSolicitudes):
    class Meta:
        proxy = True
        verbose_name = 'solicitudes de pacientes de riesgo'
        verbose_name_plural = 'Solicitudes de Pacientes de Riesgo'

@admin.register(SolicitudesRiesgo)
class SolicitudesRiesgoAdmin(admin.ModelAdmin):

    actions = ['asignar_turno']
    fields = ('paciente', 'vacuna', 'centro_vacunatorio', 'format_fecha_solicitud', 'format_fecha_estimada')
    search_fields = ('paciente__nombre', 'paciente__apellido', 'centro_vacunatorio','vacuna__nombre')
    list_display = ('nombre','apellido', 'centro_vacunatorio', 'vacuna', 'format_fecha_solicitud', 'format_fecha_estimada','boton')
    readonly_fields = ('paciente', 'vacuna', 'centro_vacunatorio', 'format_fecha_solicitud', 'format_fecha_estimada')
    list_display_links = None
    ordering = ['solicitud_id']
    
    @admin.display(description='Acciones')
    def boton(self, obj):
        # el parámetro 'obj.pk' es el id del objeto dentro de la línea, hay que pasarlo en
        # el link para saber qué objeto se va a usar, estos botones son de ejemplo y hacen lo mismo

      render_action_buttons = render_to_string('admin/pacientes_actions_buttons.html', {'pk' : obj.pk})
      return mark_safe(render_action_buttons)
  
    # función para no permitir que se añada un elemento
    def has_add_permission(self, request):
        return False

    # función para no permitir que se elimine un elemento
    def has_delete_permission(self, request, obj=None):
        return False

    # sobreescribo el método de buscado de elementos para filtrar por criterios
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        queryset = queryset.select_related('paciente').filter(solicitud_aprobada=0, paciente__es_paciente_riesgo=1)

        return queryset, use_distinct

   
    # aplico formatos a las fechas que se listan
    @admin.display(description='Fecha Solicitud')
    def format_fecha_solicitud(self, obj):
        return obj.fecha_solicitud.strftime('%d-%m-%Y')

    @admin.display(description='Fecha Sugerida')
    def format_fecha_estimada(self, obj):
        return obj.fecha_estimada.strftime('%d-%m-%Y')  

    def nombre(self,obj):
        return obj.paciente.nombre
     
    def apellido(self,obj):
        return obj.paciente.apellido  

    # registro la acción para asignar fechas a las solicitudes
    @admin.action(description='Asignar fecha a solicitudes seleccionadas')
    def asignar_turno(self, request, queryset):

        if 'apply' in request.POST:
            confirmed_date = request.POST.get('confirmed_date')
            for solicitud in queryset:
                turno = PacientesTurnos(
                    solicitud        = solicitud,
                    turno_perdido    = 0,
                    turno_pendiente  = 1,
                    turno_completado = 0,
                    fecha_confirmada = confirmed_date,
                )
                turno.save()
                solicitud.solicitud_aprobada = 1
                solicitud.save()
            messages.success(request, 'Se confirmó la fecha de turno %s para %s solicitudes.' % (confirmed_date, queryset.count()))
            return redirect('%s' % (request.get_full_path()))
        context = {'orders' : queryset}
        return render(request, 'admin/asignar_turno_intermedio.html', context)
    
    

class format_estado_turno_Filter(admin.SimpleListFilter):

    title = 'estado del turno'
    parameter_name = 'format_estado_turno'

    def lookups(self, request, model_admin):
        return (
            ('Perdido', 'Perdido'),
            ('Pendiente', 'Pendiente'),
            ('Completado', 'Completado'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'Perdido':
            return queryset.filter(turno_perdido=1)
        elif value == 'Pendiente':
            return queryset.filter(turno_pendiente=1)
        elif value == 'Completado':
            return queryset.filter(turno_completado=1)
        return queryset


class Turnos(PacientesTurnos):
    class Meta:
        proxy = True
        verbose_name = 'turnos de pacientes'
        verbose_name_plural = 'Turnos de Pacientes'

        
@admin.register(Turnos)
class TurnosAdmin(admin.ModelAdmin):
    list_display = ('format_nombre','format_apellido','format_dni','format_vacuna','format_centro_vacunatorio','fecha_confirmada','format_estado_turno',)
    list_filter = (format_estado_turno_Filter,)
    fields = ('format_nombre','format_apellido','format_dni','format_vacuna','fecha_confirmada','format_estado_turno',)
    search_fields = ('solicitud__paciente__nombre','solicitud__paciente__apellido','solicitud__paciente__dni','solicitud__vacuna__nombre','solicitud__centro_vacunatorio','fecha_confirmada',)
    readonly_fields = ('format_nombre','format_apellido','format_dni','format_vacuna','fecha_confirmada','format_estado_turno',)
    list_display_links = None


     # función para no permitir que se añada un elemento
    def has_add_permission(self, request):
        return False

    # función para no permitir que se elimine un elemento
    def has_delete_permission(self, request, obj=None):
        return False

 # sobreescribo el método de buscado de elementos para filtrar por criterios
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        queryset = queryset.select_related('solicitud')
        
        return queryset, use_distinct

    @admin.display(description='Nombre')
    def format_nombre(self, obj):
        return obj.solicitud.paciente.nombre

    @admin.display(description='Apellido')
    def format_apellido(self, obj):
        return obj.solicitud.paciente.apellido

    @admin.display(description='Dni')
    def format_dni(self, obj):
        return obj.solicitud.paciente.dni

    @admin.display(description='Vacuna')
    def format_vacuna(self, obj):
        return obj.solicitud.vacuna.nombre

    @admin.display(description='Centro')
    def format_centro_vacunatorio(self, obj):
        return obj.solicitud.centro_vacunatorio    

    @admin.display(description='Estado')
    def format_estado_turno(self, obj):
        if(obj.turno_perdido == 1):
            return "Perdido"
        elif(obj.turno_pendiente == 1):
            return "Pendiente"
        else:
            return "Completado"
    
    
    
admin.site.register(VacunasAplicadas,VacunaAdmin)
   
      