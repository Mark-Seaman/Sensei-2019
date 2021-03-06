from django.conf.urls import url
from django.contrib.auth import login, logout

from mybook.guide import SeamansGuide
from mybook.seaman import DocFileIndex, DocList, Leverage, MarkSeaman, PrivateDoc, SeamansLog
from mybook.spiritual import SpiritualDoc, SpiritualSelect
from mybook.views import *


urlpatterns = [

    # Documents
    url(r'^$',                                  DocRoot.as_view()),
    url(r'^(?P<title>[\w/\-_.]*)/Missing$',     DocMissing.as_view()),
    url(r'^(?P<title>[\w/\-_.]*)/Random$',      DocRandom.as_view()),
    url(r'^(?P<title>[\w/\-_.]*)/List$',        DocList.as_view()),
    url(r'^(?P<title>[\w/\-_.]*)/Files$',       DocFileIndex.as_view()),

    # Authentication
    url(r'^login',                              login, {'template_name': 'mybook_login.html'}, name='login'),
    url(r'^logout$',                            logout, {'next_page': '/login'}),

    # MarkSeaman
    #url(r'^MarkSeaman/booknotes/(?P<title>[\w/\-.]*)$',    BookNotes.as_view()),
    url(r'MarkSeaman/(?P<title>[\w/\-.]*)$',    MarkSeaman.as_view()),

    # Guide
    url(r'^guide/(?P<title>[\w/\-_.]*)$',       SeamansGuide.as_view()),

    # Private Pages
    url(r'^info/(?P<title>[\w/\-_.]*)$',        PrivateDoc.as_view()),
    # url(r'^homework/(?P<title>[\w/\-_.]*)$',    UncHomework.as_view()),
    # url(r'^unc/(?P<title>[\w/\-_.]*)/Test$',    UncTestResults.as_view()),

    # Seaman's Log
    url(r'^seamanslog$',                        SeamansLog.as_view()),
    url(r'^seamanslog/(?P<title>[\w/\-_.]*)$',  SeamansLog.as_view()),

    # Shrinking World
    url(r'shrinkingworld/Leverage/(?P<title>[\w/\-.]*)$', Leverage.as_view()),

    # Spiritual
    url(r'^spiritual/Index$',                   SpiritualDoc.as_view()),
    url(r'^spiritual/(?P<title>[\w\-_.]*)$',    SpiritualSelect.as_view()),
    url(r'^spiritual/(?P<title>[\w/\-_.]*)$',   SpiritualDoc.as_view()),

    # System Log
    url(r'^log$', SystemLog.as_view()),

    # Documents
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/favicon.ico')),
    url(r'^robots\.txt$',  RedirectView.as_view(url='/static/robots.txt')),
    url(r'^(?P<title>[\w/\-_.]*)$',             DocDisplay.as_view()),
]
