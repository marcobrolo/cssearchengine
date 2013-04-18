from haystack import indexes
from haystack.sites import site
from engine.models import Prof, Course
from django.db import models


class ProfIndex(indexes.SearchIndex):
    text = indexes.NgramField(document=True, use_template=True)
    last_name = indexes.NgramField(model_attr='last_name')
    first_name = indexes.NgramField(model_attr='first_name')
    prof_helpfulness = indexes.DecimalField(model_attr='helpfulness')

    def get_model(self):
        return Prof

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

    def prepare_easiness(self, obj):
        return obj.prof.easiness

    def prepare_helpfulness(self, obj):
        return obj.prof.helpfulness

    def prepare_clarity(self, obj):
        return obj.prof.clarity

    def prepare_comments(self, obj):
        return obj.prof.comments

site.register(Prof, ProfIndex)


class CourseIndex(indexes.SearchIndex):
    text = indexes.NgramField(document=True, use_template=True)
    code = indexes.NgramField(model_attr='code')
    name = indexes.NgramField(model_attr='name')
    easiness = models.DecimalField()
    helpfulness = models.DecimalField()
    clarity = models.DecimalField()
    comments = models.CharField()

    def get_model(self):
        return Course

    def prepare_easiness(self, obj):
        return obj.course.easiness

    def prepare_helpfulness(self, obj):
        return obj.course.helpfulness

    def prepare_clarity(self, obj):
        return obj.course.clarity

    def prepare_comments(self, obj):
        return obj.course.comments

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

site.register(Course, CourseIndex)


