from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
import haystack
from haystack.query import SearchQuerySet
from haystack.views import SearchView
from haystack.forms import SearchForm


admin.autodiscover()
haystack.autodiscover()

sqs = SearchQuerySet()

urlpatterns = patterns('',
    (r'^$', 'engine.views.search_page'),
    (r'^results/$', 'engine.views.results_page'),
    # Examples:
    # url(r'^$', 'cssearchengine.views.home', name='home'),
    # url(r'^cssearchengine/', include('cssearchengine.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	#Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    # url(r'search/', include('haystack.urls'))
    url(r'^test/', 'engine.views.search_view'),

    url(r'^prof_profile_result/(?P<prof_id>\d+)/$','engine.views.prof_profile_result'),

    url(r'^prof_results/$', SearchView(
        template="professor_results.html",
        searchqueryset=sqs,
        form_class=SearchForm
        ),
    name='haystack_search'),

    url(r'^search/$', SearchView(
        template="professor_results.html",
        searchqueryset=sqs,
        form_class=SearchForm
        ),
    name='haystack_search'),
)
