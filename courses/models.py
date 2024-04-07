from re import S
from django.db import models
from pkg_resources import split_sections


GRADE_CHOICES = {
        ("A", "A"),
        ("A-", "A-"),
        ("B+", "B+"),
        ("B", "B"),
        ("B-", "B-"),
        ("C+", "C+"),
        ("C", "C"),
        ("C-", "C-"),
        ("D+", "D+"),
        ("D", "D"),
        ("F", "F"),
        ("P", "P"),
        ("I", "I"),
        ("AU", "AU"),
        ("W", "W"),  
    }

class Semester(models.Model):
    class Meta:
        unique_together = ('start_from', 'end_at', 'name',)

    start_from = models.DateField()
    end_at = models.DateField()
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    
    def __repr__(self) -> str:
        return self.__str__()


class Course(models.Model):
    class Meta:
        unique_together = ('name', 'semester')
    name = models.CharField(max_length=50)
    description = models.TextField(default='Simple description')
    department = models.ForeignKey('departments.Department', on_delete=models.CASCADE)
    instructors = models.ManyToManyField('departments.Instructor')
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, null=True)
    credits = models.IntegerField(default=0)
    # sections = models.ManyToManyField('Section')

    def __str__(self):
        return self.name
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def add_course(self, name, description, department, instructors, credits):
        self.name = name
        self.description = description
        self.department = department
        self.instructors = instructors
        self.credits = credits

class Section(models.Model):
    class Meta:
        unique_together = ('course', 'section_number','section_type', 'semester', 'time')
    
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    section_number = models.IntegerField()
    instructors = models.ManyToManyField('departments.Instructor')
    section_type = models.CharField(max_length=10, default="-")
    enrolled = models.IntegerField(default=0)
    capacity = models.IntegerField(default=0)
    time = models.CharField(max_length=50, default="-")

    def __str__(self):
        return str(self.section_number)
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def add_section(self, course, section_number):
        self.course = course
        self.section_number = section_number
        self.save()

class CourseGetting(models.Model):
    class Meta:
        unique_together = ('course', 'section', 'semester', 'instructor')    

    course = models.ForeignKey(Course, on_delete=models.CASCADE, unique = False)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, null=True)
    section_type = models.CharField(max_length=10, default="-")
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, null=True)
    instructor = models.ForeignKey('departments.Instructor', on_delete=models.CASCADE, null=True)
    grade_distribution = models.JSONField(default=dict)
    average_gpa = models.FloatField(default=0, null=True)
    grade = models.CharField(choices=GRADE_CHOICES, max_length=2, default="A")
    st_dev = models.FloatField(default=0, null=True)
    median_gpa = models.FloatField(default=0, null=True)

    def add_grade(self, grade, count):
        if grade in dict(GRADE_CHOICES):
            self.grade_distribution[grade] = count
            self.save()
        else:
            raise ValueError("Invalid grade")
    
    def __str__(self):
        return str(self.course)
    
    def __repr__(self) -> str:
        return self.__str__()