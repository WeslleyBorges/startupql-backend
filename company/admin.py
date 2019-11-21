from django.contrib import admin
from .models import *


# Register your models here.
class CityAdmin(admin.ModelAdmin):
    fields = ('name',)


class TitleAdmin(admin.ModelAdmin):
    fields = ('name',)


class EmployeeAdmin(admin.ModelAdmin):
    fields = ('name', 'city', 'title',)


admin.site.register(City, CityAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Employee, EmployeeAdmin)
