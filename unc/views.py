from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import RedirectView, TemplateView, UpdateView
from django.utils.timezone import now

from tool.log import log_page
from unc.bacs import schedule_data, slides_markdown, slides_django_markdown, student_projects, weekly_agenda, get_student
from unc.models import Project, Student
# from unc.projects import test_project_page
from unc.render import *
from unc.render import render_review, render_homework_data
from unc.review import *


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


class UncDjangoSlides(TemplateView):
    template_name = 'unc_slides.html'

    def get_context_data(self, **kwargs):
        kwargs['markdown'] = slides_django_markdown(self.kwargs['lesson'])
        return kwargs


class UncLessonDisplay(TemplateView):
    template_name = 'unc_theme.html'

    def get_context_data(self, **kwargs):
        title = self.kwargs.get('title', 'Index.md')
        image_path = '/static/images/unc/django'
        doc_path = 'unc/django/%s' % title
        kwargs['text'] = document_text(doc_path, image_path)
        header = 'UNC Python Webdev', 'Lesson '+title, "/static/images/unc/Bear.200.png", 'UNC Bear', '/unc/django/Index.md'
        kwargs['header'] = dict(title=header[0], subtitle=header[1], logo=header[2], logo_text=header[3], href=header[4])
        return kwargs


class UncSkillDisplay(UncPage):
    template_name = 'unc_theme.html'

    def get_context_data(self, **kwargs):
        kwargs = super(UncSkillDisplay, self).get_context_data(**kwargs)
        doc_path = self.request.path[1:]
        student = kwargs['student']
        text = render_skill_doc(doc_path, student)
        kwargs['text'] = text
        return kwargs


class UncHomework(UncPage):
    template_name = 'unc_homework.html'

    def get_context_data(self, **kwargs):
        kwargs = super(UncHomework, self).get_context_data(**kwargs)
        student = kwargs['student']
        # kwargs['card'] = render_to_string('card.html', dict(title='Card Title', body='Card Body'))
        kwargs['weeks'] = render_weekly_views(kwargs['course'], student)
        if kwargs['student']:
            kwargs['student_info'] = render_student_info(student)
            # kwargs['homework'] = render_homework_scorecard(student)
            kwargs['skills'] = render_skills(student)
            kwargs['reviews'] = render_reviews(student)
            kwargs['projects'] = render_projects(student)
            kwargs['overview'] = render_overview(student.course.name)
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
        kwargs['plan'] = render_week(plan, kwargs['student'])
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
        kwargs['students'] = student_projects(kwargs['course'])
        return kwargs


class UncStudent(UncPage):
    model = Student
    fields = ['domain']
    template_name = 'unc_homework.html'
    success_url = '/unc/bacs200'

    def get_context_data(self, **kwargs):
        log_page(self.request)
        kwargs = super(UncStudent, self).get_context_data(**kwargs)
        student = Student.get(kwargs['pk'])
        return render_homework_data(student)


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


class UncEditReview(UpdateView):
    model = Review
    fields = ['requirement_1', 'requirement_2', 'requirement_3', 'requirement_4', 'requirement_5',
              'requirement_6', 'requirement_7', 'requirement_8', 'requirement_9', 'requirement_10', 'notes']
    template_name = 'unc_review.html'

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get('pk')
        review = get_review(pk)
        labels = [r.strip() for r in review.requirement_labels.split('\n')]
#        header = '', kwargs['object'].name, "/static/images/unc/Bear.200.png", 'UNC Bear', '/unc/bacs200'
#        header = dict(title=header[0], subtitle=header[1], logo=header[2], logo_text=header[3], href=header[4])
        kwargs = dict(title='Design Review', labels=labels)
        return super(UncEditReview, self).get_context_data(**kwargs)

    def form_valid(self, form):
        self.object.score = count_score(self.object)
        self.object.date = now()
        return super(UncEditReview, self).form_valid(form)

    def get_success_url(self):
        student = self.object.reviewer
        return '/unc/%s' % student.course.name


class UncReviews(UncPage):
    template_name = 'reviewer.html'

    def get_context_data(self, **kwargs):
        kwargs = super(UncReviews, self).get_context_data(**kwargs)
        student = Student.lookup('Sensei 350')
        kwargs['reviews'] = render_reviews(student)
        return kwargs


class UncReviewFeedback(UncPage):
    template_name = 'unc_feedback.html'

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get('pk')
        kwargs = render_review(pk)
        kwargs = super(UncReviewFeedback, self).get_context_data(**kwargs)
        return kwargs
