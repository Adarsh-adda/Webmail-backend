from django.contrib import admin
from .models import User,Mail

from import_export import resources
from import_export.admin import ImportExportModelAdmin

class MAilResource(resources.ModelResource):

    class Meta:
        model = Mail

class MailAdmin(ImportExportModelAdmin):
    resource_class = MAilResource


# Register your models here.

admin.site.register(User)
admin.site.register(Mail,MailAdmin)