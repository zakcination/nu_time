from django.contrib import admin
from .models import Semester, Course, CourseGetting, Section

class SemesterAdmin(admin.ModelAdmin):
    list_display = ('start_from', 'end_at', 'name')


class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'department', 'credits')


class CourseGettingAdmin(admin.ModelAdmin):
    list_display = ('course', 'section', 'semester', 'instructor', 'grade_distribution', 'grade', 'capacity')

class SectionAdmin(admin.ModelAdmin):
    list_display = ('course', 'section_number')


admin.site.register(Semester, SemesterAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(CourseGetting, CourseGettingAdmin)
admin.site.register(Section, SectionAdmin)
