from unc.bacs import print_projects
from unc.models import Requirement, Project


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
    create_project_record(course, '01', 'index.php', bacs200_project1_requirements())
    create_project_record(course, '02', 'bacs200/index.html', bacs200_project2_requirements())
    create_project_record(course, '03', 'bacs200/profile.html', bacs200_project1_requirements())
    return print_projects('bacs200')


def create_project_record(course, project_num, page, requirements):
    p = Project.lookup(course, project_num)
    p.page = page
    p.save()
    for i, r in enumerate(requirements):
        add_requirement(p, i + 1, r[0], r[1])

