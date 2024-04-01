import csv
from datetime import date
from datetime import datetime
from turtle import st

from courses.models import CourseGetting
from courses.models import Course
from courses.models import Section
from departments.models import Instructor
from departments.models import Department
from courses.models import Semester
import re
from departments.models import course_to_department_mapper
from django.db import IntegrityError

GRADE_VALUES = {
    "A": 4.0,
    "A-": 3.7,
    "B+": 3.3,
    "B": 3.0,
    "B-": 2.7,
    "C+": 2.3,
    "C": 2.0,
    "C-": 1.7,
    "D+": 1.3,
    "D": 1.0,
    "F": 0.0,
    "P": 0.0,
    "I": 0.0,
    "AU": 0.0,
    "W": 0.0
}

def parse_csv(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file, delimiter=',')
        filename = file_path.split('/')[-1]
        semester_name = filename.split('_')[0] + ' ' + filename.split('_')[1]
        print(semester_name)
        current_semester = Semester.objects.get(name__iexact=semester_name)
        level = filename.split('_')[2]
        next(reader)
        for row in reader:
            
            course , section_number = row[0], row[1]
            course_obj = Course.objects.get(name=course, semester=current_semester)
            section_obj = Section.objects.get(course=course_obj, section_number=section_number)
            
            # get instructor, capacity from section object by section number
            curr_instructor, curr_capacity = section_obj.instructors, section_obj.capacity

            total_grades = int(row[2])
            
            counts = calculate_counts(row, total_grades)

            ave_grade = calculate_average_gpa(counts, GRADE_VALUES, total_grades)
            

            course_getting_obj, course_getting_created = CourseGetting.objects.get_or_create(
                course=course, 
                section= section_obj,
                semester = current_semester,
                instructor = curr_instructor,
                grade_distribution = {},
                grade = ave_grade,
                capacity = curr_capacity
                )
            course_getting_obj.add_grade("A", round(counts['A']))
            course_getting_obj.add_grade("B", round(counts['B']))
            course_getting_obj.add_grade("C", round(counts['C']))
            course_getting_obj.add_grade("D", round(counts['D']))
            course_getting_obj.add_grade("F", round(counts['F']))
            course_getting_obj.add_grade("P", round(counts['P']))
            course_getting_obj.add_grade("I", round(counts['I']))
            course_getting_obj.add_grade("AU", round(counts['AU']))
            course_getting_obj.add_grade("W", round(counts['W']))
            course_getting_obj.save()
    
    print('Successfully parsed CSV file')

def extract_semester_name(file_path):
    # Implement the logic based on your file naming convention
    filename = file_path.split('/')[-1]
    semester_name = " ".join(filename.split('_')[2:4])
    print(semester_name)
    return semester_name

def calculate_grade_distribution(row):
    # Implement this based on your CSV format.
    # Example: { "A": count, "B": count, ... }
    distribution = {grade: int(row[i]) for i, grade in enumerate(["A", "B", "C", "D", "F", "P", "I", "AU", "W"], start=6)}
    return distribution

def float_to_letter_grade(grade):
                    if grade >= 4.0:
                        return "A"
                    elif grade >= 3.7:
                        return "A-"
                    elif grade >= 3.3:
                        return "B+"
                    elif grade >= 3.0:
                        return "B"
                    elif grade >= 2.7:
                        return "B-"
                    elif grade >= 2.3:
                        return "C+"
                    elif grade >= 2.0:
                        return "C"
                    elif grade >= 1.7:
                        return "C-"
                    elif grade >= 1.3:
                        return "D+"
                    elif grade >= 1.0:
                        return "D"
                    else:
                        return "F"

def parse_ug_seds_fa2023_grades(file_path):
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row

            semester_name = extract_semester_name(file_path)
            try:
                current_semester = Semester.objects.get(name__iexact=semester_name)
            except Semester.DoesNotExist:
                print(f"Semester {semester_name} not found in the database.")
                return

            for row in reader:
                course_abbr, section_number = row[0], row[1]

                #if course abbr contains a ": Lab" then it is a lab section
                if ": Lab" in course_abbr:
                    section_type = "Lb"
                #if course abbr contains a ": Lecture" then it is a lecture section
                elif ": Lecture" in course_abbr:
                    section_type = "L"
                else:
                #let section_type be any section type
                    section_type = "L"


                print(f"Processing {course_abbr} Section {section_number} in {semester_name}")
                try:
                    course_obj = Course.objects.get(name=course_abbr, semester=current_semester)
                    section_objs = Section.objects.filter(course=course_obj, section_number=section_number, section_type=section_type, semester=current_semester)
                    if len(section_objs) > 1:
                        print(f"Warning: Found {len(section_objs)} sections for {course_abbr} Section {section_number} in {semester_name}")
                    section_obj = section_objs.first()
                except (Course.DoesNotExist, Section.DoesNotExist) as e:
                    print(f"Error: {e}")
                    continue

                # Assuming your CSV has columns for grade distributions in a specific format
                # Implement the logic to calculate ave_grade and grade distributions
                total_grades = int(row[2])

                counts = calculate_counts(row, total_grades)
                ave_grade = calculate_average_gpa(counts, GRADE_VALUES, total_grades)
                grade = float_to_letter_grade(ave_grade)
                grade_distribution = calculate_grade_distribution(row)
                #row4_5 replacing , to . and converting to float if it is not empty
                st_dev = float(row[4].replace(',', '.')) if len(row[4])>0 else 0
                median_gpa = float(row[5].replace(',', '.')) if len(row[5])>0 else 0



                # Create or update CourseGetting object
                try:
                    course_getting_obj, created = CourseGetting.objects.update_or_create(
                        course=course_obj, 
                        section=section_obj,
                        semester=current_semester,
                        grade=grade,
                        st_dev=st_dev,
                        median_gpa=median_gpa,
                        defaults={
                            'instructor': section_obj.instructors.first() if section_obj else None,
                            'average_gpa': ave_grade,
                            'grade_distribution': grade_distribution
                        }
                    )
                except IntegrityError:
                    print(f"Error: IntegrityError for {course_abbr} Section {section_number} in {semester_name}")
                    continue
                
                if created:
                    print(f"Added grade distribution for {course_abbr} Section {section_number} in {semester_name}")
                else:
                    print(f"Updated grade distribution for {course_abbr} Section {section_number} in {semester_name}")

                print(
                    f"Course: {course_abbr}, Section: {section_number}, Semester: {semester_name}, "
                    f"Instructor: {course_getting_obj.instructor}, Average GPA: {ave_grade}, "
                    f"Grade Distribution: {grade_distribution}"
                )

                
def parse_university_schedule_by_degree(file_path):
    with open(file_path, 'r') as file:

        reader = csv.reader(file, delimiter=',')
        # skip header
        next(reader)

        # get the the pure filename
        filename = file_path.split('/')[-1]

        #get the first row of the csv file
        current_semester = None
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

            print(course, section_number, section_type)

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
                print(f"Skipping duplicate course {course} at {section_number, section_type} for semester {semester_name}")
                continue  # Skip this iteration and move to the next row
        
            try:
                section_obj, section_created = Section.objects.get_or_create(
                    course=course_obj, 
                    section_number=section_number,
                    section_type=section_type,
                    enrolled=section_enrolled,
                    capacity=section_capacity,
                    semester=current_semester,
                    time=time
                )
            except IntegrityError:
                print(f"Skipping duplicate section {course} at {section_number, section_type} for semester {semester_name}")
                continue

            # Add the instructors to the course after it has been created
            for instructor in instructors_list:
                course_obj.instructors.add(instructor)
                section_obj.instructors.add(instructor)  

            




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


def calculate_counts(row, total_grades):
    counts = {}
    counts['A'] = float(row[6]) * total_grades / 100
    counts['B'] = float(row[7]) * total_grades / 100
    counts['C'] = float(row[8]) * total_grades / 100
    counts['D'] = float(row[9]) * total_grades / 100
    counts['F'] = float(row[10]) * total_grades / 100
    counts['P'] = float(row[11]) * total_grades / 100
    counts['I'] = float(row[12]) * total_grades / 100
    counts['AU'] = float(row[13]) * total_grades / 100
    counts['W'] = float(row[14]) * total_grades / 100
    return counts


def get_instructor_and_capacity(course_name, section_number,section_type):
    try:
        section = Section.objects.get(course__name=course_name, section_number=section_number, section_type=section_type)
        instructor = section.instructors
        capacity = section.capacity
        return instructor, capacity
    except Section.DoesNotExist:
        return None, None


def calculate_average_gpa(grade_counts, grade_values, total_grades):
    if total_grades == 0:
        return 0
    weighted_sum = sum(count * grade_values[grade] for grade, count in grade_counts.items())
    average_gpa = weighted_sum / total_grades
    #3 scientific numbers
    average_gpa = round(average_gpa, 3)
    return average_gpa