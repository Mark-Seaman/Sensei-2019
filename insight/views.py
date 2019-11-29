from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, RedirectView, TemplateView, UpdateView


from .models import Insight
from tool.days import date_str


# Show the default view
class InsightHome(TemplateView):
    template_name = 'insight_home.html'

    def get_context_data(self, **kwargs):
        days = ['2019-11-%02d' % (d+1) for d in range(30)]
        days = [(d, Insight.lookup(d).name, Insight.lookup(d).pk) for d in days]
        return dict(days=days)


# # Show the default view
# class InsightDay(UpdateView):
#     model = Insight
#     template_name = 'insight_day.html'
#     fields = ['name', 'topic']
#
#     def get_context_data(self, **kwargs):
#         date = '%4d-%02d-%02d' % (kwargs['year'], kwargs['month'], kwargs['day'])
#         doc = 'Documents/info/history/%s' % (date.replace("-",'/'))
#         kwargs['log'] = open(doc).read()
#         kwargs['insight'] = Insight.lookup(date)
#         return kwargs


# Show the list of insights
class InsightList(ListView):
    model = Insight
    template_name = 'insight_list.html'


# Add one insight
class InsightCreate(CreateView):
    model = Insight
    template_name = 'insight_add.html'
    fields = ['name', 'topic']


# Edit a insight
class InsightUpdate(UpdateView):
    model = Insight
    template_name = 'insight_edit.html'
    fields = ['name', 'topic']

    def get_context_data(self, **kwargs):
        kwargs = super(InsightUpdate, self).get_context_data(**kwargs)
        insight = kwargs['object']
        doc = 'Documents/info/history/%s' % date_str(insight.date).replace('-','/')
        kwargs['doc'] = doc
        kwargs['log'] = open(doc).read()
        return kwargs


# Delete a insight
class InsightDelete(DeleteView):
    model = Insight
    template_name = 'insight_delete.html'
    success_url = reverse_lazy('insight-list')


# Import all insights
class InsightImport(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        Insight.import_data('insights.csv')
        return '/insight/'


# Export all insights
class InsightExport(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        Insight.export_data('insights.csv')
        return '/insight/'

