from _csv import reader

from unc.models import Course, Project
from tool.shell import text_join
from django.utils.timezone import make_aware
from datetime import datetime


def initialize_data():
    create_course('bacs200', 'Web Development Intro (Fall 2019)', 'Mark Seaman',
                  'Web Design and Development for Small Business')
    create_course('bacs350', 'Web Development Intermediate (Fall 2019)', 'Mark Seaman',
                  'Intermediate Web Development with PHP/MySQL')
    p1 = 'https://shrinking-world.com/unc/bacs200/project/01'
    create_project('bacs200', 1, 'Student Home Page', 'bacs200/index.html', '2019-08-30', p1)


def print_data():

    def print_course(c):
        return '%s, %s, %s, %s' % (c.name, c.title, c.teacher, c.description)

    def print_project(c):
        return '%s/project/%02d, %s, %s, %s' % (c.course.name, c.num, c.title, c.page, c.due.strftime("%Y-%m-%d"))

    courses = [print_course(c) for c in Course.objects.all()]
    projects = [print_project(p) for p in Project.objects.all()]
    return text_join(courses + projects)


def create_course(name, title, teacher, description):
    return Course.objects.get_or_create(name=name, title=title, teacher=teacher, description=description)[0]


def create_project(course, num, title, page, due, instructions):
    course = Course.objects.get(name=course)
    due = make_aware(datetime.strptime(due, "%Y-%m-%d"))
    project = Project.objects.get_or_create(course=course, num=num)[0]
    project.title = title
    project.page = page
    project.due = due
    project.instructions=instructions
    project.save()
    return project


def schedule(course):
    #     return "SCHEDULE FOR course"
    #
    #
    # def schedule(course):
    data_file = 'Documents/unc/%s/schedule.csv' % course
    s = []
    with open(data_file) as f:
        for row in reader(f):
            s.append(row)
    return s[0], s[1], s[2:]