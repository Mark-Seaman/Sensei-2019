from django.conf.urls import url
from django.contrib.auth import login, logout

from .views import *

urlpatterns = [

    # Authentication
    url(r'^login',                              login, {'template_name': 'mybook_login.html'}, name='login'),
    url(r'^logout$',                            logout, {'next_page': '/login'}),

    # UNC
    url(r'^(?P<title>[\w/\-_.]*)/Test$',        UncTestResults.as_view()),
    url(r'^(?P<title>[\w/\-_.]*)$',             UncHomework.as_view()),

    # Documents
    # url(r'^(?P<title>[\w/\-_.]*)$',             DocDisplay.as_view()),
]
