# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.template import Context, loader, RequestContext
from django.db import models
from models import Prof, Course, CourseRating
from haystack.forms import ModelSearchForm, HighlightedSearchForm
from haystack.query import SearchQuerySet
from haystack.views import FacetedSearchView


def search_page(request):
    return render_to_response('home.html', RequestContext(request))


def results_page(request):
    return render_to_response('results.html', RequestContext(request))


def professor_profile(request, prof_id):
    # retrieve prof info from database
    professor = Prof.objects.get(pk=prof_id)
    CR = CourseRating.objects.filter(course=prof_id)
    # return object to template so it can acess professor attributes easier
    # probably very insecure and non conventional
    return render_to_response('professor_profile.html', {'professor': professor, 'comments': CR}, context_instance=RequestContext(request))


def course_profile(request, course_id):
    course = Course.objects.get(pk=course_id)
    CR = CourseRating.objects.filter(course=course_id)

    return render_to_response('course_profile.html', {'course': course, 'comments': CR}, context_instance=RequestContext(request))


def search_view(request):
    view = FacetedSearchView(template='search_results.html')
    return view(request)
