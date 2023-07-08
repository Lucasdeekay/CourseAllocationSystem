from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Lecturer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    email = models.EmailField()
    staff_id = models.CharField(max_length=20)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.staff_id


class Course(models.Model):
    title = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    unit = models.IntegerField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.code}"


class CourseAllocation(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE)
