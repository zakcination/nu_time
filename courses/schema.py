import graphene
import django_filters
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from .models import Course

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

class Query(graphene.ObjectType):
    course = graphene.Node.Field(CourseType)
    all_courses = DjangoFilterConnectionField(CourseType)