from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, RedirectView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from mybook.views import DocDisplay
from mybook.mybook import info_menu, page_settings

from .summary import *
# from .task import save_monthly_reports


# Base
class TaskBase(LoginRequiredMixin, DocDisplay):
    site_title = "My Brain", 'Top secret documents'
    logo = "/static/images/SWS_Logo_200.jpg", 'Shrinking World Solutions'
    text = '<h1>Time Accounting</h1><p>Measuring My Life</p>'

    def get_content_data(self):
        self.title = self.kwargs.get('title', 'Index')
        self.menu = info_menu(self.title)


# --------------------------
# Records


# Delete
class TaskDelete(DeleteView):
    model = Task
    success_url = reverse_lazy('task_list')
    template_name = 'task_delete.html'


# Detail
class TaskDetail(DetailView):
    model = Task
    template_name = 'task_detail.html'


# Create
class TaskCreate(CreateView):
    model = Task
    fields = ['name', 'date', 'notes', 'hours', 'done']
    template_name = 'task_edit.html'
    success_url = reverse_lazy('task_list')


# Update
class TaskUpdate(TaskBase, UpdateView):
    model = Task
    fields = ['name', 'date', 'notes', 'hours', 'done']
    template_name = 'task_edit.html'
    success_url = reverse_lazy('task_list')


# --------------------------
# Summary


# List
class TaskList(ListView):
    model = Task
    template_name = 'task_list.html'
    site_title = "My Brain", 'Top secret documents'
    logo = "/static/images/SWS_Logo_200.jpg", 'Shrinking World Solutions'
    text = '<h1>Time Accounting</h1>'

    def get_context_data(self, **kwargs):
        activity = self.kwargs.get('activity', 'All')
        labels = Task.labels()[2:]
        types = activity_summary(activity)
        tabs = activity_summary(activity)
        context = dict(tabs=tabs, labels=labels, types=types)
        self.title = 'Tasks Details - %s' % self.kwargs.get('activity', 'All')
        self.menu = info_menu(self.title)
        settings =  page_settings(self.title, self.site_title, self.logo, self.menu, self.text)
        context.update(settings)
        return context

    def get_queryset(self):
        activity = self.kwargs['activity']
        return task_activity_details(activity)


# Time
class MyTime(TaskBase, TemplateView):
    template_name = 'task_time.html'

    def get_context_data(self, **kwargs):
        kwargs = super(MyTime, self).get_context_data(**kwargs)
        kwargs.update({
            'title': 'Time Invested',
            'time_data': time_data(),
            'data_week': time_summary(8),
            'data_month': time_summary(31),
            'data_year': time_summary(366),
            'bad_days': bad_days(),
        })
        return kwargs


# Summary
class TimeSummary(TaskBase, TemplateView):
    template_name = 'task_summary.html'

    def get_context_data(self, **kwargs):
        kwargs = super(TimeSummary, self).get_context_data(**kwargs)
        kwargs.update({
            'title': 'Time Invested',
            'time_data': time_data(),
        })
        return kwargs


# Missing
class MissingDays(TaskBase, TemplateView):
    template_name = 'task_time.html'

    def get_context_data(self, **kwargs):
        kwargs = super(MissingDays, self).get_context_data(**kwargs)
        kwargs.update({
            'title': 'Incomplete Time Log',
            'data_week': bad_days_data(8),
            'data_month': bad_days_data(31),
            'data_year': bad_days_data(366),
        })
        return kwargs


# --------------------------
# Import/Export

class TaskImport(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        task_import_files()
        return '/task/time'


class TaskExport(TaskBase, TemplateView):
    template_name = 'task_export.html'

    def get_context_data(self, **kwargs):
        kwargs = super(TaskExport, self).get_context_data(**kwargs)
        days = task_export()
        kwargs.update(dict(title='Export Tasks', days=days))
        return kwargs
