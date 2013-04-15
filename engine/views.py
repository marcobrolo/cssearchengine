# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import Context, loader, RequestContext
from django.db import models
from models import Prof
from haystack.forms import ModelSearchForm, HighlightedSearchForm
from haystack.query import SearchQuerySet
from haystack.views import SearchView

def search_page(request):
    return render_to_response('home.html', RequestContext(request))

def results_page(request):
	return render_to_response('results.html', RequestContext(request))

def prof_profile_result(request, prof_id):
	# retrieve prof info from database
	professor = Prof.objects.get(pk = prof_id)
	first_name = professor.first_name
	last_name = professor.last_name
	# return object to template so it can acess professor attributes easier
	# probably very insecure and non conventional
	return render_to_response('prof_profile_result.html', {'professor':professor})

def search_view(request):
    sqs = SearchQuerySet().all()
    view = SearchView(template='professor_results.html')
    return view(request)
