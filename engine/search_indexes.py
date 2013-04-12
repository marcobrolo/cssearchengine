from haystack import indexes
from haystack.sites import site
from engine.models import Prof



class ProfIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    last_name = indexes.CharField(model_attr='last_name')
    first_name = indexes.CharField(model_attr='first_name')

    def get_model(self):
        return Prof

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

site.register(Prof, ProfIndex)
