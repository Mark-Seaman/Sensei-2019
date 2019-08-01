from django.shortcuts import render

# Create your views here.
from mybook.mybook import document_text, homework_menu
from mybook.views import DocDisplay
from tool.page import capture_page_features


class UncHomework(DocDisplay):
    template_name = 'unc_homework.html'

    site_title = 'Homework Master', 'UNC BACS 200'
    logo = "/static/images/unc/Bear.200.png", 'UNC'

    def get_content_data(self):
        self.text = document_text('unc/bacs200/Homework')
        self.menu = homework_menu(self.kwargs.get('title', 'Index'))
        url = 'http://unco-bacs.org/bacs200/class/templates/simple.html'
        student = 'Mark Seaman'
        self.title = 'Week #1: Aug 26 - Aug 30'
        self.data = dict(student=student,
                         url=url,
                         requirements='There are no requirements.',
                         )


class UncTestResults(DocDisplay):
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