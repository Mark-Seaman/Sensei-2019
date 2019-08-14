from django.views.generic import TemplateView

from mybook.mybook import document_text, unc_menu
from tool.log import log_page
from unc.bacs import schedule_data, weekly_lessons, slides_markdown
from tool.page import validate_project_page


class UncPage(TemplateView):
    template_name = 'unc_theme.html'

    def get_context_data(self, **kwargs):
        log_page(self.request)
        course = self.kwargs.get('course','NONE')
        title = self.kwargs.get('title', 'Index')
        kwargs['menu'] = unc_menu(course, title)
        course = 'BACS 350' if course=='bacs350' else 'BACS 200'
        header = 'UNC Digital Classroom', 'UNC %s' % course, "/static/images/unc/Bear.200.png", 'UNC Bear'
        kwargs['header'] = dict(title=header[0], subtitle=header[1], logo=header[2], logo_text=header[3])
        doc_path = self.request.path[1:]
        kwargs['text'] = document_text(doc_path)
        return kwargs


class UncDocDisplay(UncPage):
    template_name = 'unc_theme.html'


class UncHomework(UncPage):
    template_name = 'unc_homework.html'

    def get_context_data(self, **kwargs):
        course = kwargs['course']
        kwargs['schedule'] = schedule_data(course)[1]
        kwargs['weeks'] = weekly_lessons(course)
        kwargs = super(UncHomework, self).get_context_data(**kwargs)
        return kwargs


class UncProject(UncPage):
    template_name = 'unc_project.html'


# class UncWeek(UncPage):
#     template_name = 'unc_week.html'
#
#     def get_content_data(self):
#         self.text = document_text('unc/bacs200/01')
#         self.menu = homework_menu(self.kwargs.get('title', 'Index'))
#         student = 'Mark Seaman'
#         self.title = 'Week #1: Aug 26 - Aug 30'
#         self.data = dict(student=student)
#

class UncSchedule(UncPage):
    template_name = 'unc_schedule.html'

    def get_context_data(self, **kwargs):
        kwargs = super(UncSchedule, self).get_context_data(**kwargs)
        kwargs['schedule'] = schedule_data(kwargs['course'])
        return kwargs


class UncSlides(UncPage):
    template_name = 'unc_slides.html'
    # template_name = 'unc_theme.html'

    def get_context_data(self, **kwargs):
        course = self.kwargs.get('course')
        lesson = self.kwargs.get('lesson')
        kwargs['markdown'] = slides_markdown(course, lesson)
        kwargs = super(UncSlides, self).get_context_data(**kwargs)
        return kwargs


class UncTestResults(UncPage):
    template_name = 'unc_test_results.html'

    def get_context_data(self, **kwargs):
        kwargs = super(UncTestResults, self).get_context_data(**kwargs)
        course = self.kwargs.get('course')
        project = self.kwargs.get('project')
        kwargs['test_results'] = validate_project_page(course, project)
        return kwargs