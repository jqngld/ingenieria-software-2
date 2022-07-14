from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.admin import AdminSite
from admin_interface.models import Theme

AdminSite.site_url = None

admin.site.unregister(Theme)
admin.site.unregister(Group)