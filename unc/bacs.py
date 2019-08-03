from _csv import reader

from unc.models import Course, Project, Lesson
from tool.shell import banner, text_join
from django.utils.timezone import make_aware
from datetime import datetime
from tool.days import parse_date, date_str


def add_project(row):
    # num = row[6] if row[6]!='' else '1'
    date = make_aware(parse_date(row[2]))
    date = date_str(date)
    page = 'bacs200/project_%s.html' % row[0]
    instructions = '/unc/bacs200/project/%s' % row[0]
    # print(date, page, instructions)
    create_project('bacs200', row[0], '1', page, date, instructions)


def add_lesson(row):
    # print(row)
    c = Course.objects.get(name='bacs200')
    p = Project.objects.get(num=row[0])
    date = make_aware(datetime.strptime(row[2], "%m/%d/%Y"))
    num = row[3] if row[3] != '' else '1'
    Lesson.objects.get_or_create(course=c, project=p, week=row[0], date=date, lesson=num, topic=row[4], reading=row[5])

    # CSV Data -- Week, Day, Date, Lesson, Topic, Reading, Projects, Process, Parts


def create_course(name, title, teacher, description):
    return Course.objects.get_or_create(name=name, title=title, teacher=teacher, description=description)[0]


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


def import_schedule(course):
    table = read_schedule(course)
    for row in table[2:-3]:
        add_project(row)
        add_lesson(row)


def init_data_test():
    initialize_data()
    print(print_data())


def initialize_data():
    create_course('bacs200', 'Web Development Intro (Fall 2019)', 'Mark Seaman',
                  'Web Design and Development for Small Business')
    create_course('bacs350', 'Web Development Intermediate (Fall 2019)', 'Mark Seaman',
                  'Intermediate Web Development with PHP/MySQL')
    p1 = 'https://shrinking-world.com/unc/bacs200/project/01'
    import_schedule('bacs200')


def print_data():
    courses = [banner('Courses')] + Course.list()
    projects = [banner('Projects')] + Project.list()
    lessons = [banner('Lessons')] + Lesson.list()
    return text_join(courses + projects + lessons)


def read_schedule(course):
    data_file = 'Documents/unc/%s/schedule.csv' % course
    with open(data_file) as f:
        return [row[:-2] for row in reader(f)]


def schedule_data(course):
    data_file = 'Documents/unc/%s/schedule.csv' % course
    s = []
    with open(data_file) as f:
        for row in reader(f):
            s.append(row)
    return s[0], s[1], s[2:]


