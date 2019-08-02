from django.views.generic import TemplateView

from mybook.mybook import document_text, homework_menu
from tool.page import capture_page_features
from tool.log import log_page
from unc.bacs import schedule_data


class UncPage(TemplateView):
    template_name = 'unc_theme.html'

    def get_context_data(self, **kwargs):
        log_page(self.request)
        header = 'UNC Digital Classroom', 'UNC BACS 200', "/static/images/unc/Bear.200.png", 'UNC Bear'
        kwargs['header'] = dict(title=header[0], subtitle=header[1], logo=header[2], logo_text=header[3])
        doc_path = self.request.path[1:]
        kwargs['text'] = document_text(doc_path)
        kwargs['menu'] = homework_menu(self.kwargs.get('title', 'Index'))
        return kwargs


class UncDocDisplay(UncPage):
    template_name = 'unc_theme.html'


class UncHomework(UncPage):
    template_name = 'unc_homework.html'


class UncProject(UncPage):
    template_name = 'unc_project.html'


class UncWeek(UncPage):
    template_name = 'unc_week.html'

    def get_content_data(self):
        self.text = document_text('unc/bacs200/01')
        self.menu = homework_menu(self.kwargs.get('title', 'Index'))
        student = 'Mark Seaman'
        self.title = 'Week #1: Aug 26 - Aug 30'
        self.data = dict(student=student)


class UncSchedule(UncPage):
    template_name = 'unc_schedule.html'

    def get_context_data(self, **kwargs):
        kwargs = super(UncSchedule, self).get_context_data(**kwargs)
        kwargs['schedule'] = schedule_data(kwargs['course'])
        return kwargs


class UncSlidesDisplay(UncPage):
    template_name = 'unc_slides.html'

    def get_context_data(self, **kwargs):
        title = self.kwargs.get('title')
        course  = self.kwargs.get('course')
        text = slides_markdown(title)
        return site_settings(title=title, course=course, markdown=text)


class UncTestResults(UncPage):
    template_name = 'unc_test_results.html'
    site_title = 'Homework Master', 'UNC BACS 200'
    logo = "/static/images/unc/Bear.200.png", 'UNC'

    def get_content_data(self):

        self.menu = homework_menu(self.kwargs.get('title', 'Index'))
        self.text = document_text('unc/bacs200/project/01')
        self.title = 'Test Results: Project #1'

        url = 'http://unco-bacs.org'
        requirements = ['head', 'body', 'h1', 'title']
        results, source = capture_page_features(url, requirements)
        student = 'Mark Seaman'

        self.data = dict(student=student,
                         url=url,
                         requirements=requirements,
                         test_results=results,
                         source=source)