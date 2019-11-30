from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, RedirectView, TemplateView, UpdateView

from .models import Insight
from .insight import export_data, group_insights, import_data
from tool.days import date_str


# Show the default view
class InsightHome(TemplateView):
    template_name = 'insight_home.html'

    def get_context_data(self, **kwargs):
        days = ['2019-11-%02d' % (d+1) for d in range(30)]
        days = [(d, Insight.lookup(d).name, Insight.lookup(d).pk) for d in days]
        return dict(days=days)


# Show the list of insights
class InsightList(TemplateView):
    template_name = 'insight_list.html'

    def get_context_data(self, **kwargs):
        kwargs = super(InsightList, self).get_context_data(**kwargs)
        kwargs['insights'] = group_insights()
        return kwargs


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
        import_data('insights.csv')
        return '/insight/'


# Export all insights
class InsightExport(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        export_data('insights.csv')
        return '/insight/'

