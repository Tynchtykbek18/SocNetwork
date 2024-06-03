from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Course(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="courses")
    course = models.SmallIntegerField(default=1)

    def __str__(self):
        return f"{self.course}"


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    day = models.CharField(max_length=255)
    time = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    teacher = models.CharField(max_length=255, null=True, blank=True)
    room = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.name}"
