from django.db import models
from courses.models import Course

# [ Courses ] Semester : Start_from(dateField), ends_at(dateField), name(Charfield20)

DEPARTMENT_CHOICES = {
    ("SEDS", "SEDS | School of Engineering and Digital Sciences"),
    ("SSH", "SSH | School of Sciences and Humanities"),
    ("SMG","SMG | School of Mining and Geosciences"),
    ("GSPP","GSPP | Graduate School of Public Policy"),
    ("GSE","GSE | Graduate School of Education"),
    ("GSB", "GSB | Graduate School of Business"),
    ("NUSOM","NUSOM | School of Medicine"),
    ("CPS","CPS | Center for Preparatory Studies"), 
}

COURSE_PREFIX_TO_DEPARTMENT_MAP = {
    'CSCI': 'SEDS',
    'CEE': 'SEDS',
    'CHME': 'SEDS',
    'ELCE': 'SEDS',
    'ENG': 'SEDS',
    'MAE': 'SEDS',
    'ROBT': 'SEDS',
    'ANT': 'SSH',
    'BIOL': 'SSH',
    'CHEM': 'SSH',
    'CHN': 'SSH',
    'ECON': 'SSH',
    'FRE': 'SSH',
    'GER': 'SSH',
    'HST': 'SSH',
    'KAZ': 'SSH',
    'LING': 'SSH',
    'MATH': 'SSH',
    'PER': 'SSH',
    'PHIL': 'SSH',
    'PHYS': 'SSH',
    'PLS': 'SSH',
    'REL': 'SSH',
    'SOC': 'SSH',
    'SPA': 'SSH',
    'SSH': 'SSH',
    'TUR': 'SSH',
    'WCS': 'SSH',
    'KOR': 'SSH',
    'RFL': 'SSH',
    'KFL': 'SSH',
    'WLL': 'SSH',
    'DUT': 'SSH',
    'GEOL': 'SMG',
    'MINE': 'SMG',
    'PETE': 'SMG',
    'SMG': 'SMG',
    'BUS': 'GSB',
    'FIN': 'GSB',
    'ACCT': 'GSB',
    'NUR': 'NUSOM',
    'NUSM': 'NUSOM'
}

class Instructor(models.Model):
    class Meta:
        unique_together = ('first_name', 'last_name', 'middle_name',)
    
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    def __repr__(self) -> str:
        return self.__str__()


class Department(models.Model):
    # class Meta:
    #     unique_together = ('name')
    name = models.CharField(max_length=6, choices=DEPARTMENT_CHOICES, unique=True)

    def __str__(self):
        return self.name
    
    def __repr__(self) -> str:
        return self.__str__()


class Major(models.Model):
    class Meta:
        unique_together = ('name', 'department',)

    name = models.CharField(max_length=50)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    def __repr__(self) -> str:
        return self.__str__()
    
    
# create all departments
# departments = ["SEDS", "SSH", "SMG", "GSPP", "GSE", "GSB", "NUSOM", "CPS"]
# for department in departments:
#     Department.objects.get_or_create(name=department)

# create all majors
    
def course_to_department_mapper(name):
    for prefix, department_name in COURSE_PREFIX_TO_DEPARTMENT_MAP.items():
        if name.startswith(prefix):
            try:
                return Department.objects.get(name=department_name)
            except Department.DoesNotExist:
                return None
    return None