from datetime import datetime
from os.path import join

from django.utils.timezone import make_aware, now

from tool.days import parse_date, date_str
from tool.page import open_browser_dom, close_browser_dom, capture_page, capture_page_features, display_test_results
from tool.shell import banner
from tool.text import text_join
from unc.models import Requirement, Project, Course, Assignment


def add_requirement(project, id, selector, transform):
    r = Requirement.objects.get_or_create(project=project, selector=selector)[0]
    r.num = id
    r.label = selector
    r.transform = transform
    r.save()
    return r


def bacs200_project1_requirements():
    return [
        ('html', 'count_chars(r.actual, 10000, 20000)'),
        ('head', 'count_chars(r.actual, 5000, 6000)'),
        ('head title', ''),
        ('body', 'count_lines(r.actual, 50, 200)'),
        ('body header h1', ''),
        ('h3', ''),
        ('p', ''),
    ]


def bacs200_project2_requirements():
    return [
        ('head', 'count_chars(r.actual, 80, 85)'),
        ('head title', 'count_chars(r.actual, 15, 30)'),
        ('body', 'count_lines(r.actual, 20, 30)'),
        ('body h1', 'count_chars(r.actual, 20, 30)'),
        ('h2', ''),
        ('p', ''),
    ]


def build_projects(course):
    create_project_record(course, '01', 'index.php',            bacs200_project1_requirements())
    create_project_record(course, '02', 'bacs200/index.html',   bacs200_project2_requirements())
    create_project_record(course, '03', 'bacs200/profile.html', bacs200_project1_requirements())
    return list_project_details('bacs200')


def create_project_record(course, project_num, page, requirements):
    p = Project.lookup(course, project_num)
    p.page = page
    p.save()
    for i, r in enumerate(requirements):
        add_requirement(p, i + 1, r[0], r[1])


def add_project(course, row):

    def create_project(course, num, title, page, due, instructions):
        course = Course.objects.get(name=course)
        due = make_aware(datetime.strptime(due, "%Y-%m-%d"))
        project = Project.objects.get_or_create(course=course, num=num)[0]
        project.title = title
        project.page = page
        project.due = due
        project.instructions = instructions
        project.save()
        return project

    date = make_aware(parse_date(row[2]))
    date = date_str(date)
    page = '%s/project_%s.html' % (course, row[0])
    instructions = '/unc/%s/project/%s' % (course, row[0])
    title = row[6]
    return create_project(course, row[0], title, page, date, instructions)


def print_assignments(course):
    assigned = ['\n%s Assignments: ' % course]
    for h in Assignment.objects.filter(project__course__name=course):
        assigned.append(str(h))
    return text_join(assigned)


def list_project_details(course):
    results = []
    for p in Project.objects.filter(course__name=course).order_by('due'):
        results.append('\nProject %s' % p)
        for r in p.requirements:
            results.append('    selector=%s, transform=%s' % (r.selector, r.transform))
    return results


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