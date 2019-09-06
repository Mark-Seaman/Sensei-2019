from django.utils.timezone import make_aware, now
from os.path import join

from tool.days import parse_date, date_str, due_date
from tool.page import open_browser_dom, close_browser_dom, capture_page, capture_page_features, display_test_results
from tool.shell import banner
from tool.text import text_join
from unc.models import Assignment, Course, Lesson, Project, Requirement, Student


def add_assignment(course, student, project, due):
    p = Project.lookup(course, project)
    a = Assignment.objects.get_or_create(project=p, student=student, score=0, due=due_date(due), status=0)[0]
    a.date = now()
    a.save()


def assignment_due(course, student, project, due):
    p = Project.lookup(course, project)
    a = Assignment.objects.get(project=p, student=student)
    a.due = due_date(due)
    a.score = 0
    a.status = 0
    a.save()


def add_project(course, row):
    def create_project(course, num, title, page, due, instructions):
        course = Course.objects.get(name=course)
        due = due_date(due)
        project = Project.objects.get_or_create(course=course, num=num)[0]
        project.title = title
        project.page = page
        project.due = due
        project.instructions = instructions
        project.save()
        return project

    date = make_aware(parse_date(row[2]))
    date = date_str(date)
    page = '%s/project/%s' % (course, row[0])
    instructions = '/unc/%s/project/%s' % (course, row[0])
    title = row[6] if row[6:] else 'None'
    return create_project(course, row[0], title, page, date, instructions)


def add_requirement(project, id, selector, transform):
    r = Requirement.objects.get_or_create(project=project, selector=selector)[0]
    r.num = id
    r.label = selector
    r.transform = transform
    r.save()
    return r


def add_test_assignments():
    course = 'cs350'
    assign_homework(course, '01', '2019-08-30')
    assign_homework(course, '02', '2019-09-06')
    # clear_assignments()


def approve_requirements(course, id):
    project = Project.lookup(course, id)
    for i, r in enumerate(project.requirements):
        r.correct = r.actual
        r.save()


def assign_homework(course, project, due):
    for s in Course.students(course):
        add_assignment(course, s, project, due)


def assign_project_1():
    for c in Course.all():
        assign_homework(c, '01', '2019-08-30')


def build_projects(course):
    create_project_record(course, '01', 'index.php', fake_project_requirements())
    create_project_record(course, '02', 'bacs350/index.html', fake_project_requirements())
    # create_project_record(course, '03', 'bacs350/profile.html', bacs200_project1_requirements())
    return list_project_details(course)


def clear_assignments():
    Assignment.objects.all().delete()


def create_project_record(course, project_num, page, requirements):
    p = Project.lookup(course, project_num)
    p.page = page
    p.save()
    for i, r in enumerate(requirements):
        add_requirement(p, i + 1, r[0], r[1])


def fake_project_requirements():
    return [
        ('html', 'count_chars(r.actual, 1, 10)'),
        # ('head', 'count_chars(r.actual, 5000, 6000)'),
        # ('head title', ''),
        # ('body', 'count_lines(r.actual, 50, 200)'),
        # ('body header h1', ''),
        # ('h3', ''),
        # ('p', ''),
        # ('head', 'count_chars(r.actual, 80, 85)'),
        # ('head title', 'count_chars(r.actual, 15, 30)'),
        # ('body', 'count_lines(r.actual, 20, 30)'),
        # ('body h1', 'count_chars(r.actual, 20, 30)'),
        # ('h2', ''),
        # ('p', ''),
    ]


# from unc.models import *

def fix_domains():
    for s in Student.objects.filter():
        if s.domain != 'No Domain Configured':
            if not s.domain.startswith('http'):
                s.domain = 'http://'+s.domain
                s.save()
                print(s.domain)

# fix_domains()


def fix_project_pages():
    course = 'bacs200'
    create_project_record(course, '01', 'index.php',            fake_project_requirements())
    create_project_record(course, '02', 'bacs200/inspire.html', fake_project_requirements())
    course = 'bacs350'
    create_project_record(course, '01', 'index.php',            fake_project_requirements())
    create_project_record(course, '02', 'bacs350/index.php',    fake_project_requirements())
    return list_project_details(course)


def get_assignments(student):
    def assigned(a):
        link = '<a href="/unc/%s/project/%02d">Project #%s</a>' % (
        a.project.course.name, a.project.num, a.project.title)
        return dict(title=link, due=date_str(a.due), state=a.state)

    return [assigned(a) for a in Assignment.objects.filter(student=student)]


def get_readings(student):
    def assigned(a):
        return dict(title="Reading - %s" % a.reading, due=date_str(a.date), state='Not Completed')

    def lessons(course, date):
        return Lesson.query(course).filter(date__lte=due_date(date))

    return [assigned(a) for a in lessons(student.course.name, '2019-08-30')]


def list_assignments(course):
    assigned = ['\n\nAssignments for %s:           project          due            status         last update\n' % course]
    for h in Assignment.objects.filter(project__course__name=course):
        assigned.append(str(h))
    return text_join(assigned)


def list_project_details(course):
    results = []
    for p in Project.objects.filter(course__name=course).order_by('due'):
        results.append('\nProject %s' % p)
        for r in p.requirements:
            results.append('    selector=%s, transform=%s' % (r.selector, r.transform))
    return text_join(results)


def show_assignments():
    return text_join([list_assignments(c) for c in Course.all()])


def test_project_page(student, project):
    if student:
        dom = open_browser_dom()
        data = validate_project_page(dom, student, project)
        close_browser_dom(dom)
        return data


def validate_project_page(dom, student, project):
    p = Project.lookup(student.course.name, project)
    url = join(student.domain, p.page)
    source = capture_page(dom, url)
    requirements = capture_page_features(dom, p.requirements)
    student = 'Mark Seaman'
    return dict(student=student, url=url, requirements=requirements, source=source, date=now())


def validate_unc_project(dom, student, project, ):
    return banner('PROJECT %s' % project) + display_test_results(validate_project_page(dom, student, project))


