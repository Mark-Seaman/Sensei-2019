from django.contrib.auth import logout
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import RedirectView, TemplateView, UpdateView

from mybook.mybook import document_text
from tool.log import log_page
from unc.bacs import schedule_data, slides_markdown, student_data, weekly_agenda, get_student
from unc.models import Student
from unc.projects import test_project_page
from unc.render import render_homework_scorecard, render_student_info, render_weekly_agenda, render_course_agenda, \
    render_skill_doc, render_skills


class UncPage(LoginRequiredMixin, TemplateView):
    template_name = 'unc_theme.html'

    def get_context_data(self, **kwargs):
        log_page(self.request)
        student = get_student(self.request)
        if student:
            name = student.name
        else:
            name = 'Not logged in'
        course = self.kwargs.get('course', 'NONE')
        href = '/unc/' + course
        course = 'BACS 350' if course == 'bacs350' else 'BACS 200'
        header = 'UNC %s' % course, name, "/static/images/unc/Bear.200.png", 'UNC Bear', href
        kwargs['header'] = dict(title=header[0], subtitle=header[1], logo=header[2], logo_text=header[3],
                                href=header[4])
        kwargs['student'] = student
        return kwargs


class UncDocDisplay(UncPage):
    template_name = 'unc_theme.html'

    def get_context_data(self, **kwargs):
        kwargs = super(UncDocDisplay, self).get_context_data(**kwargs)
        doc_path = self.request.path[1:]
        image_path = '/static/images/unc/bacs200' if 'bacs200' == kwargs['course'] else '/static/images/unc/bacs350'
        kwargs['text'] = document_text(doc_path, image_path)
        return kwargs


class UncSkillDisplay(UncPage):
    template_name = 'unc_theme.html'

    def get_context_data(self, **kwargs):
        kwargs = super(UncSkillDisplay, self).get_context_data(**kwargs)
        doc_path = self.request.path[1:]
        student = kwargs['student']
        # lesson = kwargs['lesson']
        text = render_skill_doc(doc_path, student)
        # image_path = '/static/images/unc/bacs200' if 'bacs200' == kwargs['course'] else '/static/images/unc/bacs350'
        # text = document_text(doc_path, image_path)
        # skills_path = '%s' % ()
        # text = text.replace('{{ skills }}', 'xxx')
        kwargs['text'] = text
        return kwargs


class UncHomework(UncPage):
    template_name = 'unc_homework.html'

    def get_context_data(self, **kwargs):
        kwargs = super(UncHomework, self).get_context_data(**kwargs)
        student = kwargs['student']
        # kwargs['card'] = render_to_string('card.html', dict(title='Card Title', body='Card Body'))
        kwargs['weeks'] = render_course_agenda(kwargs['course'], student)
        if kwargs['student']:
            kwargs['student_info'] = render_student_info(student)
            kwargs['homework'] = render_homework_scorecard(student)
            kwargs['skills'] = render_skills(student)
        return kwargs


class UncLogout(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        logout(self.request)
        return '/unc/login/'


class UncProject(UncPage):
    template_name = 'unc_project.html'


class UncWeek(UncPage):
    template_name = 'unc_week.html'

    def get_context_data(self, **kwargs):
        kwargs = super(UncWeek, self).get_context_data(**kwargs)
        plan = weekly_agenda(kwargs['course'], int(kwargs['week']))
        kwargs['plan'] = render_weekly_agenda(plan, kwargs['student'])
        return kwargs


class UncSchedule(UncPage):
    template_name = 'unc_schedule.html'

    def get_context_data(self, **kwargs):
        kwargs = super(UncSchedule, self).get_context_data(**kwargs)
        kwargs['schedule'] = schedule_data(kwargs['course'])
        return kwargs


class UncStudents(UncPage):
    template_name = 'unc_students.html'

    def get_context_data(self, **kwargs):
        kwargs = super(UncStudents, self).get_context_data(**kwargs)
        kwargs['students'] = student_data(kwargs['course'])
        return kwargs


class UncStudent(UpdateView):
    model = Student
    fields = ['domain']
    template_name = 'unc_student.html'
    success_url = '/unc/bacs200'

    def get_context_data(self, **kwargs):
        log_page(self.request)
        kwargs = super(UncStudent, self).get_context_data(**kwargs)
        header = 'UNC Student Profile', kwargs[
            'object'].name, "/static/images/unc/Bear.200.png", 'UNC Bear', '/unc/bacs200'
        kwargs['header'] = dict(title=header[0], subtitle=header[1], logo=header[2], logo_text=header[3],
                                href=header[4])
        return kwargs


class UncSlides(UncPage):
    template_name = 'unc_slides.html'

    def get_context_data(self, **kwargs):
        kwargs = super(UncSlides, self).get_context_data(**kwargs)
        kwargs['markdown'] = slides_markdown(kwargs['course'], kwargs['lesson'])
        return kwargs


class UncTestResults(UncPage):
    template_name = 'unc_test_results.html'

    def get_context_data(self, **kwargs):
        kwargs = super(UncTestResults, self).get_context_data(**kwargs)
        project = self.kwargs.get('project')
        student = get_student(self.request)
        kwargs['test_results'] = test_project_page(student, project)
        return kwargs
