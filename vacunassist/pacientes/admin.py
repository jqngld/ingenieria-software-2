from django.contrib import admin
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import *
from django.utils.html import mark_safe
from django.urls import reverse
from django.utils.safestring import mark_safe  

from datetime import date
from dateutil.relativedelta import relativedelta

# admin.site.register(Usuarios)
# admin.site.register(VacunasDetalles)
# admin.site.register(PacientesTurnos)
# admin.site.register(PacientesDetalles)
# admin.site.register(PacientesSolicitudes)
# admin.site.register(VacunasAplicadas) 


class VacunaAdmin(admin.ModelAdmin):      
      fields = ('vacuna','lote','paciente')
      list_filter = ('vacuna','lote','paciente', 'fecha_vacunacion')
      list_display = ('vacuna','lote','nombrePaciente','apellido','fecha_vacunacion')  
      search_fields = ('paciente__nombre','paciente__apellido','vacuna__nombre') 
      
      
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
    # actions = ['list_admins']
    list_display = ('format_nombre','format_apellido','format_dni','edad','email','format_centro_vacunatorio','boton')
    search_fields = ('email','pacientesdetalles__nombre','pacientesdetalles__apellido','pacientesdetalles__dni', 'pacientesdetalles__centro_vacunatorio')
    

    
    
    
    @admin.display(description='Acciones')
    def boton(self, obj):
        # el parámetro 'obj.pk' es el id del objeto dentro de la línea, hay que pasarlo en
        # el link para saber qué objeto se va a usar, estos botones son de ejemplo y hacen lo mismo

        link_change_info = "'http://127.0.0.1:8000/admin/pacientes/vacunasaplicadas/%s/change/'" % (obj.pk)
        

        return mark_safe(\
                '\
                <button type="button" title="Cambiar Contraseña" onclick="window.location.href=%s" class="btn btn-success btn-sm" name="apply"><i class="bi bi-key"></i></button>\
                <button type="button" title="Editar Información" onclick="window.location.href=%s" class="btn btn-success btn-sm" name="apply"><i class="bi bi-pencil"></i></button>\
                ' % ("" , link_change_info)\
                )
    


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

    @admin.display(description='Nombre')
    def format_nombre(self, obj):
        return obj.pacientesdetalles.nombre

    @admin.display(description='Apellido')
    def format_apellido(self, obj):
        return obj.pacientesdetalles.apellido

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
    list_filter = ('paciente__nombre', 'paciente__apellido', 'centro_vacunatorio')
    search_fields = ('paciente__nombre', 'paciente__apellido', 'centro_vacunatorio','vacuna__nombre')
    list_display = ('nombre','apellido' ,'centro_vacunatorio', 'vacuna', 'format_fecha_solicitud', 'format_fecha_estimada')
    readonly_fields = ('paciente', 'vacuna', 'centro_vacunatorio', 'format_fecha_solicitud', 'format_fecha_estimada')


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


class SolicitudesRiesgo(PacientesSolicitudes):
    class Meta:
        proxy = True
        verbose_name = 'solicitudes de pacientes de riesgo'
        verbose_name_plural = 'Solicitudes de Pacientes de Riesgo'

@admin.register(SolicitudesRiesgo)
class SolicitudesRiesgoAdmin(admin.ModelAdmin):

    actions = ['asignar_turno']
    fields = ('paciente', 'vacuna', 'centro_vacunatorio', 'format_fecha_solicitud', 'format_fecha_estimada')
    list_filter = ('paciente__nombre', 'paciente__apellido', 'centro_vacunatorio')
    list_display = ('paciente', 'centro_vacunatorio', 'vacuna', 'format_fecha_solicitud', 'format_fecha_estimada')
    readonly_fields = ('paciente', 'vacuna', 'centro_vacunatorio', 'format_fecha_solicitud', 'format_fecha_estimada')


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
    
    
    
    
    
admin.site.register(VacunasAplicadas,VacunaAdmin)
   
      