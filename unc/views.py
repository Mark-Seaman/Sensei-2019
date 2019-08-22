from django.template.loader import render_to_string
from django.views.generic import TemplateView

from mybook.mybook import document_text, unc_menu
from tool.log import log_page
from unc.bacs import schedule_data, slides_markdown, student_data, test_project_page, weekly_agenda, weekly_lessons, get_student


def render_student_info(student):
    return render_to_string('student.html', dict(student=student))


def render_project(project, student):
    return render_to_string('project.html', dict(project=project, student=student))


def render_lessons(lessons):
    return ''.join([render_to_string('lesson.html', dict(lesson=x)) for x in lessons])


def render_weekly_agenda(plan, student):
    project = render_project(plan['project'], student)
    lessons = render_lessons(plan['lessons'])
    weekly_plan = dict(week=plan['week'], project=project, lessons=lessons)
    return render_to_string('week.html', weekly_plan)


def render_course_agenda(course, student):
    weeks = weekly_lessons(course)
    return [(w['week'], render_weekly_agenda(w, student)) for w in weeks]


class UncPage(TemplateView):
    template_name = 'unc_theme.html'

    def get_context_data(self, **kwargs):
        log_page(self.request)
        student = get_student(self.request)
        if student:
            name = student.name
        else:
            name = 'Not logged in'
        course = self.kwargs.get('course','NONE')
        title = self.kwargs.get('title', 'Index')
        kwargs['menu'] = unc_menu(course, title)
        course = 'BACS 350' if course=='bacs350' else 'BACS 200'
        href = '/unc/bacs200'
        header = 'UNC %s' % course, name, "/static/images/unc/Bear.200.png", 'UNC Bear', href
        kwargs['header'] = dict(title=header[0], subtitle=header[1], logo=header[2], logo_text=header[3], href=header[4])
        kwargs['student'] = student
        doc_path = self.request.path[1:]
        kwargs['text'] = document_text(doc_path)
        return kwargs


class UncDocDisplay(UncPage):
    template_name = 'unc_theme.html'


class UncHomework(UncPage):
    template_name = 'unc_homework.html'

    def get_context_data(self, **kwargs):
        kwargs = super(UncHomework, self).get_context_data(**kwargs)
        # kwargs['card'] = render_to_string('card.html', dict(title='Card Title', body='Card Body'))
        kwargs['weeks'] = render_course_agenda(kwargs['course'], kwargs['student'])
        kwargs['student_info'] = render_student_info(kwargs['student'])
        return kwargs


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


class UncSlides(UncPage):
    template_name = 'unc_slides.html'

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
        project = self.kwargs.get('project')
        student = get_student(self.request)
        kwargs['test_results'] = test_project_page(student, project)
        return kwargs