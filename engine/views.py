# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import Context, loader, RequestContext

def search_page(request):
    return render_to_response('home.html', RequestContext(request))

def results_page(request):
		return render_to_response('results.html', RequestContext(request))
