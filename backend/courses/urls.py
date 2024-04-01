# courses/urls.py
from django.urls import path
from .views import CourseListView
from .views import SemesterListView

urlpatterns = [
    path('courses/', CourseListView.as_view(), name='course-list'),
    path('semesters/', SemesterListView.as_view(), name='semester-list'),
]
