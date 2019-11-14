from django.conf.urls import url
# from django.contrib import auth
from django.urls import include

from .views import *
from .urlgame import UncUrlGameAnswer, UncUrlGameQuestion, UncUrlGameDone

urlpatterns = [

    # Authentication
    url(r'^logout', UncLogout.as_view()),
    url(r'^', include('django.contrib.auth.urls')),

    url(r'^django/(?P<lesson>\d\d)/slides$',                UncDjangoSlides.as_view()),
    url(r'^django/(?P<title>[\w/\-_.]+)$',                  UncLessonDisplay.as_view()),

    url(r'^(?P<course>[-_ \w]+)/week/(?P<week>\d\d)$',      UncWeek.as_view()),

    url(r'student/(?P<pk>\d+)$',                            UncStudent.as_view()),
    url(r'^(?P<course>[-_ \w]+)/students$',                 UncStudents.as_view()),
    url(r'^(?P<course>[-_ \w]+)/(?P<project>\d\d)/test$',   UncTestResults.as_view()),
    url(r'^(?P<course>[-_ \w]+)/schedule$',                 UncSchedule.as_view()),

    url(r'^(?P<course>[-_ \w]+)/(?P<lesson>\d\d)/slides$',  UncSlides.as_view()),
    url(r'^(?P<course>[-_ \w]+)/skills/(?P<lesson>\d\d)$',  UncSkillDisplay.as_view()),

    url(r'^review/(?P<pk>[\d]+)$',                          UncEditReview.as_view()),
    # url(r'^reviews$',                                     UncReviews.as_view()),
    url(r'^feedback/(?P<pk>[\d]+)$',                        UncReviewFeedback.as_view()),

    url(r'^url-question$',                                  UncUrlGameQuestion.as_view()),
    url(r'^url-answer$',                                    UncUrlGameAnswer.as_view()),
    url(r'^url-game-done$',                                 UncUrlGameDone.as_view()),

    url(r'^(?P<course>[-_ \w]+)/(?P<title>[\w/\-_.]+)$',    UncDocDisplay.as_view()),
    url(r'^(?P<course>[-_ \w]+)$',                          UncHomework.as_view()),

]
