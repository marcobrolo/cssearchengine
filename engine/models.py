from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.


class Prof(models.Model):
    last_name = models.CharField(max_length=20)
    first_name = models.CharField(max_length=20)
    helpfulness = models.DecimalField(max_digits=2, decimal_places=1)
    clarity = models.DecimalField(max_digits=2, decimal_places=1)
    easiness = models.DecimalField(max_digits=2, decimal_places=1)
    home_page = models.CharField(max_length=20)
    profile_page = models.CharField(max_length=20)
    def __unicode__(self):
        return self.fullname()

    def get_absolute_url(self):
        return reverse('engine.views.professor_profile', kwargs={'prof_id': self.id})

    def fullname(self):
        if self.last_name:
            return u"%s, %s" % (self.last_name, self.first_name)


class Course(models.Model): 
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=40)

    def __unicode__(self):
        return self.title()

    def title(self):
        if self.code:
            return u"%s %s" % (self.code, self.name)

    def get_absolute_url(self):
        return reverse('engine.views.course_profile', kwargs={'course_id': self.id})


class CourseRating(models.Model): 
    course = models.ForeignKey('Course', related_name='course')
    prof = models.ForeignKey('Prof', related_name='prof')
    easiness = models.IntegerField(default=0)
    helpfulness = models.IntegerField(default=0)
    clarity = models.IntegerField(default=0)
    comments = models.TextField()

    def __unicode__(self):
        return self.course
