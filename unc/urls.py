from django.conf.urls import url
from django.contrib.auth import login, logout

from .views import *

urlpatterns = [

    # Authentication
    url(r'^login',                              login, {'template_name': 'mybook_login.html'}, name='login'),
    url(r'^logout$',                            logout, {'next_page': '/login'}),

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
