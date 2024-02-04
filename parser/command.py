import csv
from datetime import date
from datetime import datetime
from courses.models import CourseGetting
from courses.models import Course
from courses.models import Section
from departments.models import Instructor
from departments.models import Department
from courses.models import Semester
import re
from departments.models import course_to_department_mapper
from django.db import IntegrityError



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


def parse_university_schedule_by_degree(file_path):
    with open(file_path, 'r') as file:

        reader = csv.reader(file, delimiter=',')
        # skip header
        next(reader)

        # get the the pure filename
        filename = file_path.split('/')[-1]

        #get the first row of the csv file

        # Semester.name and Level
        semester_name = filename.split('_')[2] + ' 20' + filename.split('_')[3]
        # level = filename.split('_')[2]
        obj = ''
        count = 0
        for row in reader:
            if count == 0:
                count += 1
                sem_start = str(row[5]) # 08-JAN-24
                # reformating the date 19-APR-24 to DateField of Django
                formatted_sem_start_date = date_formatter(sem_start)
                
                sem_end = str(row[6]) # 19-APR-24
                formatted_sem_end_date = date_formatter(sem_end)

                current_semester, semester_created = Semester.objects.get_or_create(name=semester_name, start_from=formatted_sem_start_date, end_at=formatted_sem_end_date)
                continue

            # Get Course Abbr
            course = str(row[0])
            if course == '':
                continue
            # Get Section number & Section type 1L and 2Lb
            # for section_number get the the number part of the string
            section = row[1]
            section_number, section_type = get_section_number_and_type(section)

            section_number = str(section_number)
            section_type = str(section_type)

            # Get course title
            title = str(row[2]) 

            # Get ECTS
            credits = str(row[4])
            if credits == '':
                credits = '0'

            sem_start = str(row[5])

            sem_end = str(row[6])

            days = str(row[7])

            time = str(row[8])

            section_enrolled = str(row[9])

            section_capacity = str(row[10])

            # Get Instructor
            instructors = str(row[11])
            #remove /n from the string
            instructors = instructors.replace('\n', '')

            # Get Room
            room = str(row[12])
            #remove /n from the string
            room = room.replace('\n', '')

            instructors = split_instructors(instructors)
            instructors_list = []
            for instructor in instructors:
                first_name, last_name = instructor.split(' ', 1)
                instructor_obj, instructor_created = Instructor.objects.get_or_create(
                    first_name=first_name.strip(), 
                    last_name=last_name.strip()
                )
                instructors_list.append(instructor_obj)

            department = course_to_department_mapper(course)

            try:
                course_obj, course_created = Course.objects.get_or_create(
                    name = course,
                    description = title,
                    department = department, 
                    credits = credits,
                    semester = current_semester
                )
            except IntegrityError:
                try:
                    course = Course.objects.get(name='Nonexistent Course')
                except Course.DoesNotExist:
                    course = None
                
            Section_obj, section_created = Section.objects.get_or_create(
                course=course_obj, 
                section_number=section_number,
                section_type=section_type,
                enrolled=section_enrolled,
                capacity=section_capacity,
            )

            # Add the instructors to the course after it has been created
            for instructor in instructors_list:
                course_obj.instructors.add(instructor)    

            




    print('Successfully parsed CSV file')

def get_section_number_and_type(section):
    match = re.match(r'(\d+)(\D+)', section)
    if match:
        return match.groups()
    else:
        return None, None
    

def date_formatter(date_string):
    date_object = datetime.strptime(date_string, "%d-%b-%y")
    formatted_date = date_object.strftime("%Y-%m-%d")
    return formatted_date


def format_schedule_file(file):
    # remove new lines from the column
    filename = file.split('/')[-1]
    formatted_rows = []
    with open(file, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            for i in range(len(row)):
                row[i] = row[i].replace('\n', '')
            formatted_rows.append(row)

    # save file as a new file at the same deirectory
    with open('parser/resources/' + 'formatted_' + filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(formatted_rows)

    print('Successfully formatted the file and saved as formatted_' + filename)


def split_instructors(instructors):
    # Split the instructors by comma
    instructors = instructors.split(',')

    for i in range(len(instructors)):
        # Insert a space before each uppercase letter that is not at the start of the string
        instructors[i] = re.sub(r'(?<!^)(?=[A-Z])', ' ', instructors[i])

    return instructors
