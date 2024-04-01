# courses/serializers.py
from rest_framework import serializers
from .models import Course
from .models import Semester

class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = ['id', 'name', 'start_from', 'end_at']

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'credits', 'department', 'Instructors', 'semester']  # Adjust the fields as needed
