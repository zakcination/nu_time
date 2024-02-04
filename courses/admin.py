from django.contrib import admin
from .models import Semester, Course, CourseGetting, Section

class SemesterAdmin(admin.ModelAdmin):
    list_display = ('start_from', 'end_at', 'name')


class CourseAdmin(admin.ModelAdmin):
    list_display = ('semester','department', 'name', 'description','total_sections','display_instructors','credits')

    def total_sections(self, obj):
        return obj.section_set.count()
    total_sections.short_description = 'Total Sections'

    def display_instructors(self, obj):
        return ", ".join([str(instructor) for instructor in obj.instructors.all()])
    display_instructors.short_description = 'Instructors'


class CourseGettingAdmin(admin.ModelAdmin):
    list_display = ('course', 'section', 'semester', 'instructor', 'grade_distribution', 'grade', 'capacity')

class SectionAdmin(admin.ModelAdmin):
    list_display = ('course', 'section_number', 'section_type', 'enrolled', 'capacity')
    ordering = ('course',)

    def total_enrolled(self, obj):
        return sum(section.enrolled for section in obj.section_set.all())
    total_enrolled.short_description = 'Total Enrolled'

    def total_capacity(self, obj):
        return sum(section.capacity for section in obj.section_set.all())
    total_capacity.short_description = 'Total Capacity'


admin.site.register(Semester, SemesterAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(CourseGetting, CourseGettingAdmin)
admin.site.register(Section, SectionAdmin)
