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


def _checkNone(item):
    if item is None:
        return 0.0
    return item


def find_best_prof_for_course(course_id):
    # find the best prof for the given courseID
    best_prof = ''
    best_avg = 0.0
    clarity = 0.0
    easiness = 0.0
    helpfulness = 0.0
    best_clarity = {'clarity__avg': 0.0}
    best_easiness = {'easiness__avg': 0.0}
    best_helpfulness = {'helpfulness__avg': 0.0}
    course = Course.objects.get(pk=course_id)
    CR = CourseRating.objects.filter(course=course_id)
    list_of_profs = [] #list of prof ids who have taught this course before
    for possible_Profs in CR:
        # fill list of profs who've taught this course
        if possible_Profs.prof_id =='':
            print"ERROR"
            return "NULL", "NULL", best_clarity, best_easiness, best_helpfulness
        if possible_Profs.prof_id not in list_of_profs:
            list_of_profs.append(possible_Profs.prof_id)
    #print "prof list", list_of_profs
    # go through the list and find the prof with best avg score
    for profID in list_of_profs:
        overall = 0
        PR = CR.filter(prof=profID)
        # find the prof's average
        helpfulness = PR.aggregate(Avg('helpfulness'))
        clarity = PR.aggregate(Avg('clarity'))
        easiness = PR.aggregate(Avg('easiness'))
        if not (clarity['clarity__avg'] is None or helpfulness['helpfulness__avg'] is None or  easiness['easiness__avg'] is None):
            overall = (clarity['clarity__avg'] + helpfulness['helpfulness__avg'] + easiness['easiness__avg'] )/3
        # compare the average to current best average, to see which prof is better
        if best_avg < overall:
            best_avg = overall
            best_prof = profID
            best_clarity = clarity
            best_easiness = easiness
            best_helpfulness = helpfulness
        # now we have the best prof and his score, return it
    #print best_prof, best_avg
    return best_prof, best_avg, best_helpfulness, best_clarity, best_easiness


def search_page(request):
    return render_to_response('home.html', RequestContext(request))


def results_page(request):
    return render_to_response('results.html', RequestContext(request))


def professor_profile(request, prof_id):
    # retrieve prof info from database
    overall = "NULL"
    professor = Prof.objects.get(pk=prof_id)
    CR = CourseRating.objects.filter(prof=prof_id)
    helpfulness = _checkNone(professor.helpfulness)
    clarity = _checkNone(professor.clarity)
    easiness = _checkNone(professor.easiness)
    overall = (clarity + helpfulness + easiness) / 3
    pics_root  = '../static/pics/'
    profilepic = 'placeholder.png'
    print pics_root + professor.first_name.lower() + professor.last_name.lower()
    try:
        open(pics_root + professor.first_name.lower() + professor.last_name.lower() + '.jpg', 'r')
        profilepic = professor.first_name.lower() + professor.last_name.lower() + '.jpg'
    except IOError:
        pass
    context = {
        'professor': professor,
        'overall': overall,
        'comments': CR,
        'pic': profilepic
    }
    return render_to_response('professor_profile.html', context, context_instance=RequestContext(request))


def course_profile(request, course_id):
    course = Course.objects.get(pk=course_id)
    CR = CourseRating.objects.filter(course=course_id)
    best_prof = ''
    # figure out whos best prof and his score for this course
    best_prof_id, best_avg, helpfulness, clarity, easiness = find_best_prof_for_course(course_id)
    # do edge case, if no RMP record of any prof teaching this course
    try:
        best_prof = Prof.objects.get(pk=best_prof_id) # find the best prof obj from id
    except:
        disclaimer = "No record of proffesors teaching this course, rate now!"
        best_prof = Prof.objects.create(first_name=disclaimer, last_name="", helpfulness='0', clarity ='0', easiness='0')
        print("NO PROF FOR THIS COURSE?", best_prof_id)

    #print "best prof is ", best_prof.first_name, best_prof.last_name, best_avg

    #clarity = CourseRating.objects.filter(course=course_id).aggregate(Avg('clarity'))
    #helpfulness = CourseRating.objects.filter(course=course_id).aggregate(Avg('helpfulness'))
    #easiness = CourseRating.objects.filter(course=course_id).aggregate(Avg('easiness'))

    #overall = 0
    #if not (clarity['clarity__avg'] is None or helpfulness['helpfulness__avg'] is None or  easiness['easiness__avg'] is None):
    #	overall = (clarity['clarity__avg'] + helpfulness['helpfulness__avg'] + easiness['easiness__avg'] )/3

    context = {
        'course': course,
        'comments': CR,
        'clarity': clarity['clarity__avg'],
		'helpfulness': helpfulness['helpfulness__avg'],
		'easiness': easiness['easiness__avg'],
		'overall': best_avg,
        'best_prof': best_prof
    }
    return render_to_response('course_profile.html', context, context_instance=RequestContext(request))


def search_view(request):
    view = FacetedSearchView(template='search_results.html')
    return view(request)
