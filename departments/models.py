from django.db import models

# [ Courses ] Semester : Start_from(dateField), ends_at(dateField), name(Charfield20)


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
    name = models.CharField(max_length=50, unique=True)

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