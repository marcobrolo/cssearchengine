from haystack import indexes
from haystack.sites import site
from models import Prof


class ProfIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True)
    last_name = indexes.CharField(model_attr='last_name')
    first_name = indexes.CharField(model_attr='first_name')
    quality = indexes.DecimalField(model_attr='quality')
    course_name = indexes.CharField(model_attr='course_name')
    course_code = indexes.CharField(model_attr='course_code')
    helpfulness = indexes.DecimalField(model_attr='helpfulness')
    clarity = indexes.DecimalField(model_attr='clarity')
    easiness = indexes.DecimalField(model_attr='easiness')
    comments = indexes.CharField(model_attr='comments')

    def prepare(self, obj):
        self.prepared_data = super(ProfIndex, self).prepare(obj)
        return self.prepared_data


site.register(Prof, ProfIndex)
