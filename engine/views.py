# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.template import Context, loader, RequestContext
from django.db import models
from django.db.models import Avg
from models import Prof, Course, CourseRating
from haystack.forms import ModelSearchForm, HighlightedSearchForm
from haystack.query import SearchQuerySet
from haystack.views import FacetedSearchView
from django.contrib.humanize.templatetags.humanize import intcomma


def search_page(request):
    return render_to_response('home.html', RequestContext(request))


def results_page(request):
    return render_to_response('results.html', RequestContext(request))


def professor_profile(request, prof_id):
    # retrieve prof info from database
    professor = Prof.objects.get(pk=prof_id)
    CR = CourseRating.objects.filter(prof=prof_id)
    # return object to template so it can acess professor attributes easier
    # probably very insecure and non conventional
    return render_to_response('professor_profile.html', {'professor': professor, 'comments': CR}, context_instance=RequestContext(request))


def course_profile(request, course_id):
    course = Course.objects.get(pk=course_id)
    CR = CourseRating.objects.filter(course=course_id)

    clarity = CourseRating.objects.filter(course=course_id).aggregate(Avg('clarity'))
    helpfulness = CourseRating.objects.filter(course=course_id).aggregate(Avg('helpfulness'))
    easiness = CourseRating.objects.filter(course=course_id).aggregate(Avg('easiness'))
    
    overall = 0
    if not (clarity['clarity__avg']  is None or helpfulness['helpfulness__avg'] is None or  easiness['easiness__avg'] is None):
    	overall = (clarity['clarity__avg'] + helpfulness['helpfulness__avg'] + easiness['easiness__avg'] )/3

    context = {
            'course': course,
            'comments': CR,
            'clarity': clarity['clarity__avg'],
    		'helpfulness': helpfulness['helpfulness__avg'],
    		'easiness': easiness['easiness__avg'],
    		'overall': overall
    }
    return render_to_response('course_profile.html', context, context_instance=RequestContext(request))


def search_view(request):
    view = FacetedSearchView(template='search_results.html')
    return view(request)
