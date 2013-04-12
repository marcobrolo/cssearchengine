from django.db import models
# Create your models here.


class Prof(models.Model):
    last_name = models.CharField(max_length=20)
    first_name = models.CharField(max_length=20)
    helpfulness = models.DecimalField(max_digits=2, decimal_places=1)
    clarity = models.DecimalField(max_digits=2, decimal_places=1)
    easiness = models.DecimalField(max_digits=2, decimal_places=1)
    comments = models.CharField(max_length=600)


class Course(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=40)


class CourseRating(models.Model):
    course = models.ForeignKey('Course')
    prof = models.ForeignKey('Prof')
    easiness = models.IntegerField(default=0)
    helpfulness = models.IntegerField(default=0)
    clarity = models.IntegerField(default=0)
