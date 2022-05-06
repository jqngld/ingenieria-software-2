from django.contrib import admin
from django.urls import path
from paciente.views import saludo
urlpatterns = [
    path('admin/', admin.site.urls),
    path('saludo/',saludo),

]