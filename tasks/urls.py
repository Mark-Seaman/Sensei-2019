from django.conf.urls import url

from tasks.views import TaskDetail, TaskCreate, TaskList, TaskUpdate, TaskDelete, TaskExport, TaskImport, MyTime, TimeSummary, MissingDays

urlpatterns = [

    # Records

    url(r'^add$',                   TaskCreate.as_view(), name='task_add'),
    url(r'(?P<pk>\d+)/edit$',       TaskUpdate.as_view(), name='task_update'),
    url(r'(?P<pk>\d+)/delete$',     TaskDelete.as_view(), name='task_delete'),
    url(r'^(?P<pk>\d+)$',           TaskDetail.as_view(), name='task-detail'),

    # Import
    url(r'^import$',                TaskImport.as_view(), name='task_import'),
    url(r'^export$',                TaskExport.as_view()),

    # Time Summary
    # url(r'^$',                          TaskHome.as_view()),
    url(r'^summary$',                   TimeSummary.as_view()),
    url(r'^time$',                      MyTime.as_view()),
    url(r'^bad$',                       MissingDays.as_view()),
    url(r'^(?P<activity>[\w\d\-\.]*)$', TaskList.as_view(), name='task_list'),

]
