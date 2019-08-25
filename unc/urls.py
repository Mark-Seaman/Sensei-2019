from django.conf.urls import url
# from django.contrib import auth
from django.urls import include

from .views import *

urlpatterns = [

    # Authentication
    url(r'^', include('django.contrib.auth.urls')),

    # url(r'^(?P<course>[-_ \w]+)/(?P<title>[\w/\-_.]*)/project$', UncProject.as_view()),
    # url(r'^(?P<course>[-_ \w]+)/(?P<week>\d\d)/(?P<title>[\w/\-_.]*)$',        UncWeek.as_view()),
    url(r'^(?P<course>[-_ \w]+)/week/(?P<week>\d\d)$',      UncWeek.as_view()),

    url(r'student/(?P<pk>\d+)$',                            UncStudent.as_view()),
    url(r'^(?P<course>[-_ \w]+)/students$',                 UncStudents.as_view()),
    url(r'^(?P<course>[-_ \w]+)/(?P<project>\d\d)/test$',   UncTestResults.as_view()),
    url(r'^(?P<course>[-_ \w]+)/schedule$',                 UncSchedule.as_view()),

    url(r'^(?P<course>[-_ \w]+)/(?P<lesson>\d\d)/slides$',  UncSlides.as_view()),

    url(r'^(?P<course>[-_ \w]+)/(?P<title>[\w/\-_.]+)$',    UncDocDisplay.as_view()),
    url(r'^(?P<course>[-_ \w]+)$',                          UncHomework.as_view()),

]
