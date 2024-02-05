from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

from .models import Course
from .models import Section
from .models import Semester

# render to json

import datetime


def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

# get all courses from coures.models.Course json
def course_catalog(request, course_name=''):
    if course_name == '':
        courses = Course.objects.all()
    else:
        courses = Course.objects.filter(name=course_name)
    return JsonResponse(list(courses.values()), safe=False)

# get all sections from coures.models.Section json
def section_catalog(request, course_name=''):
    if course_name == '':
        sections = Section.objects.all()
    else:
        sections = Section.objects.filter(course__name=course_name)
    return JsonResponse(list(sections.values()), safe=False)

#get all semesters from coures.models.Semester json
def semester_catalog(request):
    semesters = Semester.objects.all()
    return JsonResponse(list(semesters.values()), safe=False)
