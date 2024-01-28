import csv
from datetime import date
from courses.models import CourseGetting
from courses.models import Course
from courses.models import Section
from departments.models import Instructor
from departments.models import Department
from courses.models import Semester



def parse_csv(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file, delimiter=',')
        dummy_instructor, instructor_created = Instructor.objects.get_or_create(first_name="Dummy", last_name="Instructor")
        dummy_department, department_created = Department.objects.get_or_create(name = "Dummy Department")
        dummy_description = "Dummy description"
        dummy_semester, semester_created = Semester.objects.get_or_create(start_from=date.today(), end_at=date.today(), name="Dummy Semester")
        # skip header
        next(reader)
        for row in reader:
            #obj = ''
            course, course_created = Course.objects.get_or_create(
                name = str(row[0]),
                description = dummy_description,
                department = dummy_department, 
                credits = 0
            )
            course.instructors.set([dummy_instructor])
            section, section_created = Section.objects.get_or_create(
                course=course, 
                section_number=row[1])
            # obj += str(row[0]) + ' | '
            # obj += str(row[1])  + ' | '
            total_grades = int(row[2])
            # obj += str(total_grades) + ' | '
            #obj += '['

            #generate JSONfield instance of grades
            countA = float(row[6]) * total_grades / 100
            # obj += 'A : ' + str(round(countA))
            countB = float(row[7]) * total_grades / 100
            # obj += ', B : ' + str(round(countB))
            countC = float(row[8]) * total_grades / 100
            #obj += ', C : ' + str(round(countC))
            countD = float(row[9]) * total_grades / 100
            #obj += ', D : ' + str(round(countD))
            countF = float(row[10]) * total_grades / 100
            #obj += ', F : ' + str(round(countF))
            countP = float(row[11]) * total_grades / 100
            #obj += ', P : ' + str(round(countP))
            countI = float(row[12]) * total_grades / 100
            #obj += ', I : ' + str(round(countI))
            countAU = float(row[13]) * total_grades / 100
            #obj += ', AU : ' + str(round(countAU))
            countW = float(row[14]) * total_grades / 100
            #obj += ', W : ' + str(round(countW))
            course_getting_obj, course_getting_created = CourseGetting.objects.get_or_create(
                course=course, 
                section=section, 
                semester = dummy_semester,
                instructor = dummy_instructor,
                grade_distribution = {},
                grade = 'A',
                capacity = total_grades
                )
            course_getting_obj.add_grade("A", round(countA))
            course_getting_obj.add_grade("B", round(countB))
            course_getting_obj.add_grade("C", round(countC))
            course_getting_obj.add_grade("D", round(countD))
            course_getting_obj.add_grade("F", round(countF))
            course_getting_obj.add_grade("P", round(countP))
            course_getting_obj.add_grade("I", round(countI))
            course_getting_obj.add_grade("AU", round(countAU))
            course_getting_obj.add_grade("W", round(countW))

            #obj += ']'
            #print(obj)
            course_getting_obj.save()
    
    print('Successfully parsed CSV file')
