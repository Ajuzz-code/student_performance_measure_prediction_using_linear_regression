from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    name = models.CharField(max_length=100)
    #code = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    roll_no = models.CharField(max_length=20,default="NA")
    year = models.IntegerField()
    contact = models.CharField(max_length=15)
    address = models.TextField(default="Not Provided")

    def __str__(self):
        return self.user.username


class Prediction(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    #study_hours = models.FloatField()
    attendance = models.FloatField()
    previous_marks = models.FloatField()
    assignments = models.FloatField()
    absences = models.FloatField()
    predicted_marks = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)
    def grade(self):
        if self.predicted_marks < 40:
            return "Fail"
        elif self.predicted_marks < 60:
            return "Pass"
        elif self.predicted_marks < 75:
            return "First Class"
        else:
            return "Distinction"

    def probability(self):
        # Convert marks to probability (0–1)
        return round(self.predicted_marks / 100, 2)
