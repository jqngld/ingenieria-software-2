from django.urls import path
from django.contrib import admin
from administrador.views import *

# admin.site.password_change_template = 'admin/change_password.html'
# admin.site.password_change_done_template = 'admin/change_password_done.html'

admin.site.index_template = 'admin/index.html'

urlpatterns = [
    path('', home_admin, name='home_admin'),

]