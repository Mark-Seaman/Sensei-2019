from csv import reader
from re import compile

from unc.models import Course, Project, Lesson
from tool.shell import banner, text_join
from django.utils.timezone import make_aware
from datetime import datetime
from tool.days import parse_date, date_str


def add_project(row):
    date = make_aware(parse_date(row[2]))
    date = date_str(date)
    page = 'bacs200/project_%s.html' % row[0]
    instructions = '/unc/bacs200/project/%s' % row[0]
    title = 'Project %s' % row[0]
    # print(date, page, instructions)
    return create_project('bacs200', row[0], title, page, date, instructions)


def add_lesson(row):

    # CSV Data -- Week, Day, Date, Lesson, Topic, Reading, Projects, Process, Parts
    # print(row)
    project = add_project(row)
    date = make_aware(datetime.strptime(row[2], "%m/%d/%Y"))
    num = row[3] if row[3] != '' else '-1'
    # print('create lesson (course=%s, lesson %s)' % (project.course.name, num))
    # print('date: %s' % date)
    lesson = Lesson.objects.get_or_create(course=project.course, lesson=num, date=date)[0]
    lesson.week = row[0]
    lesson.project = project
    lesson.topic = row[4]
    lesson.reading = zybooks_link(row[5])
    lesson.save()
    return lesson


def zybooks_link(reading):
    # print(reading)
    match_pattern = r'^(\d+).(\d+) (.*)$'
    replace_pattern = r'<a href="https://learn.zybooks.com/zybook/UNCOBACS200SeamanFall2019/chapter/\1/section/\2">\1.\2 - \3</a>'
    link = compile(match_pattern).sub(replace_pattern, reading)
    # print(link)
    return link


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
        add_lesson(row)


def init_data_test():
    initialize_data()
    print(print_data())


def initialize_data():
    create_course('bacs200', 'Web Development Intro (Fall 2019)', 'Mark Seaman',
                  'Web Design and Development for Small Business')
    create_course('bacs350', 'Web Development Intermediate (Fall 2019)', 'Mark Seaman',
                  'Intermediate Web Development with PHP/MySQL')
    import_schedule('bacs200')


def print_data():
    courses = [banner('Courses')] + Course.list()
    projects = [banner('Projects')] + Project.list()
    lessons = [banner('Lessons')] + Lesson.list('bacs200') + Lesson.list('bacs350')
    return text_join(courses + projects + lessons)


def read_schedule(course):
    data_file = 'Documents/unc/%s/schedule.csv' % course
    with open(data_file) as f:
        return [row[:-2] for row in reader(f)]


def schedule_data(course):
    title = Course.objects.get(name=course).title
    return [title, 'Class Schedule'], Lesson.query(course)


def weekly_lessons(course):
    weeks = []
    for w in range(15):
        week = w + 1
        weeks.append(Lesson.objects.filter(course__name=course, week=week).order_by('date'))
    return weeks

