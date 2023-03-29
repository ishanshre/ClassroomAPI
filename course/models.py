from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.



User = get_user_model()


class Course(models.Model):
    title = models.CharField(max_length=255)
    code = models.CharField(max_length=255, unique=True)
    description = models.TextField(max_length=10000, null=True, blank=True)
    preview_pic = models.ImageField(upload_to="course/preview_pic", default="default/preview.jpeg")
    section = models.CharField(max_length=255, null=True, blank=True)
    subject = models.CharField(max_length=255, null=True, blank=True)
    room = models.CharField(max_length=255, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="courses")
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title
    


class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="student_in_course")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="course_as_student")

    def __str__(self):
        return f"{self.user.username.title()} enrolled in course {self.course.title.title()} as student"


class Teacher(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="teacher_in_course")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_as_teacher')

    def __str__(self):
        return f"{self.user.username.title()} enrolled in course {self.course.title.title()} as teacher"
