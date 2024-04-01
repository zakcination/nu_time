from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse


from rest_framework import generics
from .serializers import CourseSerializer
from .serializers import SemesterSerializer


from .models import Course
from .models import Section
from .models import Semester

# render to json

import datetime



def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)


class CourseListView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class SemesterListView(generics.ListAPIView):
    queryset = Semester.objects.all()
    serializer_class = SemesterSerializer


# get all sections from coures.models.Section json
def section_catalog(request, course_name=''):
    if course_name == '':
        sections = Section.objects.all()
    else:
        sections = Section.objects.filter(course__name=course_name)
    return JsonResponse(list(sections.values()), safe=False)
