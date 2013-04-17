from haystack import indexes
from haystack.sites import site
from engine.models import Prof, Course
from django.db import models


class ProfIndex(indexes.SearchIndex):
    text = indexes.NgramField(document=True, use_template=True)
    last_name = indexes.NgramField(model_attr='last_name')
    first_name = indexes.NgramField(model_attr='first_name')
    #helpfulness = indexes.DecimalField(model_attr='helpfulness')

    def get_model(self):
        return Prof

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

site.register(Prof, ProfIndex)


class CourseIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    code = indexes.CharField(model_attr='code')
    name = indexes.CharField(model_attr='name')

    def get_model(self):
        return Course

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

site.register(Course, CourseIndex)
