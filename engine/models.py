from django.db import models
# Create your models here.

class Prof(models.Model)
    last_name = models.CharField(max_length = 20)
    first_name = models.CharField(max_length = 20)
    quality = models.DecimalField(max_digits = 2 , decimal_places = 1)
    course_name = models.CharField(max_length = 50)
    course_code = models.CharField(max_length = 7)
    helpfulness = models.DecimalField(max_digits = 2 , decimal_places = 1)
    clarity = models.DecimalField(max_digits = 2 , decimal_places = 1)
    easiness = models.DecimalField(max_digits = 2 , decimal_places = 1)
    comments = models.CharField(max_length = 600)