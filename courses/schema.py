import graphene
import django_filters
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from .models import (
    Course, Semester, Section, CourseGetting
)

class CourseFilter(django_filters.FilterSet):
    class Meta: 
        model = Course
        fields = {
            'name': ['exact', 'icontains', 'istartswith'],
            'description': ['exact', 'icontains'],
            'department': ['exact'],
            'instructors': ['exact'],
            'semester': ['exact'],
            'credits': ['exact', 'lt', 'gt'],
        }

class CourseType(DjangoObjectType):
    class Meta:
        model = Course
        filterset_class = CourseFilter
        interfaces = (graphene.Node, )

class SemesterFilter(django_filters.FilterSet):
    class Meta:
        model = Semester
        fields = {
            'name': ['exact', 'icontains', 'istartswith'],
            'start_from': ['exact', 'lt', 'gt'],
            'end_at': ['exact', 'lt', 'gt'],
        }

class SemesterType(DjangoObjectType):
    class Meta:
        model = Semester
        filterset_class = SemesterFilter
        interfaces = (graphene.Node, )

class SectionFilter(django_filters.FilterSet):
    class Meta:
        model = Section
        fields = {
            'semester': ['exact'],
            'course': ['exact'],
            'section_number': ['exact', 'lt', 'gt'],
            'instructors': ['exact'],
            'section_type': ['exact', 'icontains', 'istartswith'],
            'enrolled': ['exact', 'lt', 'gt'],
            'capacity': ['exact', 'lt', 'gt'],
            'time': ['exact', 'icontains', 'istartswith'],
        }

class SectionType(DjangoObjectType):
    class Meta:
        model = Section
        filterset_class = SectionFilter
        interfaces = (graphene.Node, )

class Query(graphene.ObjectType):
    course = graphene.Node.Field(CourseType)
    all_courses = DjangoFilterConnectionField(CourseType)
    
    semester = graphene.Node.Field(SemesterType)
    all_semesters = DjangoFilterConnectionField(SemesterType)

    section = graphene.Node.Field(SectionType)
    all_sections = DjangoFilterConnectionField(SectionType)