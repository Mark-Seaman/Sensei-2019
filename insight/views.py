from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, RedirectView, TemplateView, UpdateView
from django.template.loader import render_to_string

from insight.insight import monthly_insights, task_history
from .models import Insight
from .insight import export_data, group_insights, import_data


# # Show the insights for each category
# class InsightHome(TemplateView):
#     template_name = 'insight_home.html'
#
#     def get_context_data(self, **kwargs):
#         insights = render_to_string('insight_groups.html', dict(insights=group_insights()))
#         return dict(insights=insights)


# Show the insights for each category
class InsightMonths(TemplateView):
    template_name = 'insight_months.html'

    def get_context_data(self, **kwargs):
        months = ['10', '11']
        return monthly_insights(months)


# Show the list of insights
class InsightList(TemplateView):
    template_name = 'insight_home.html'

    def get_context_data(self, **kwargs):
        insights = render_to_string('insight_groups.html', dict(insights=group_insights()))
        return dict(insights=insights)


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
        doc = task_history(insight)
        kwargs['doc'] = doc
        kwargs['log'] = open(doc).read()
        return kwargs


# # Delete a insight
# class InsightDelete(DeleteView):
#     model = Insight
#     template_name = 'insight_delete.html'
#     success_url = reverse_lazy('insight-list')


# Import all insights
class InsightImport(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        import_data('insights.csv')
        return reverse_lazy('insight-list')


# Export all insights
class InsightExport(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        export_data('insights.csv')
        return reverse_lazy('insight-list')

