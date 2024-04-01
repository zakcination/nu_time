from django.contrib import admin
from .models import Instructor, Department, Major

class InstructorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'middle_name')


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)


class MajorAdmin(admin.ModelAdmin):
    list_display = ('name', 'department')

admin.site.register(Instructor, InstructorAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Major, MajorAdmin)
