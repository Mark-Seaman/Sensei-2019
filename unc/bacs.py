from csv import reader
from datetime import datetime

from django.contrib.auth.models import User
from django.utils.timezone import make_aware, now
from os.path import join
from re import compile

from tool.days import parse_date, date_str
from tool.document import fix_images, read_markdown
from tool.log import log_exception
from tool.page import display_test_results, open_browser_dom, close_browser_dom, capture_page, capture_page_features
from tool.shell import banner, text_join
from tool.user import add_user_login, list_user_login, list_users
from unc.models import Assignment, Course, Project, Lesson, Requirement, Student


def add_assignment(course, student, project):
    c = Course.lookup(course)
    p = Project.objects.get(course=c, num=int(project))
    date = p.due
    Assignment.objects.get_or_create(project=p,
                                     student=student,
                                     score=0,
                                     date=date,
                                     status=0)


def add_lesson(course, row):
    # CSV Data -- Week, Day, Date, Lesson, Topic, Reading, Projects, Process, Parts
    # print(row)
    project = add_project(course, row)
    date = make_aware(parse_date(row[2]))
    num = row[3] if row[3] != '' else '-1'
    lesson = Lesson.objects.get_or_create(course=project.course, lesson=num, date=date)[0]
    lesson.week = row[0]
    lesson.project = project
    lesson.topic = row[4]
    lesson.reading = zybooks_link(course[-3:], row[5])
    lesson.save()
    return lesson


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


def add_student(name, email, domain, course):
    course = Course.lookup(course)
    s = Student.objects.get_or_create(name=name, email=email, course=course)[0]
    u = add_user_login(name, email)
    s.user = u
    s.domain = domain
    s.save()
    return s


# approve_requirements('bacs200', 1)
def approve_requirements(course, id):
    project = Project.lookup(course, id)
    for i, r in enumerate(project.requirements):
        r.correct = r.actual
        r.save()


def assign_homework(course, project):
    for s in Course.students(course):
        # print('assign ', course, s.name, project)
        add_assignment(course, s, project)


def clear_assignments():
    Assignment.objects.all().delete()


def create_course(name, title, teacher, description):
    return Course.objects.get_or_create(name=name, title=title, teacher=teacher, description=description)[0]


def get_student(request):
    try:
        if not request.user.is_anonymous:
            return Student.objects.get(user=request.user)
    except:
        log_exception('Cannot find student record, %s' % str(request.user))


def import_students(course):

    def read_students(course):
        data_file = 'Documents/unc/%s/students.csv' % course
        with open(data_file) as f:
            return [row for row in reader(f)]

    def display_student(course, row):
        print('%s %-40s %-15s %s' % (course, row[0], row[2], row[3]))

    table = read_students(course)
    for row in table:
        display_student(course, row)


def import_schedule(course):

    table = read_schedule(course)
    for row in table[2:]:
        add_lesson(course, row)


def import_test_students():
    course = 'bacs200'
    add_student('Tony Stark',       'mark.b.seaman+iron_man@gmail.com',     r'https://unco-bacs.org/iron_man',      course)
    add_student('Natasha Romanov ', 'mark.b.seaman+black_widow@gmail.com',  r'https://unco-bacs.org/black_widow',   course)
    add_student('Bruce Banner',     'mark.b.seaman+hulk@gmail.com',         r'https://unco-bacs.org/hulk',          course)
    course = 'bacs350'
    add_student('Steve Rogers',     'mark.b.seaman+cap@gmail.com',          r'https://unco-bacs.org/cap_america',   course)
    add_student('Carol Danvers',    'mark.b.seaman+marvel@gmail.com',       r'https://unco-bacs.org/cap_marvel',    course)
    add_student('Wanda Maximoff',   'mark.b.seaman+witch@gmail.com',        r'https://unco-bacs.org/scarlet_witch', course)


def init_data_test():
    initialize_data()
    print(print_data())


def initialize_data():
    create_course('bacs200', 'Web Development Intro (Fall 2019)', 'Mark Seaman',
                  'Web Design and Development for Small Business')
    create_course('bacs350', 'Web Development Intermediate (Fall 2019)', 'Mark Seaman',
                  'Intermediate Web Development with PHP/MySQL')
    import_schedule('bacs200')
    import_schedule('bacs350')


def print_assignments(course):
    assigned = ['\n%s Assignments: ' % course]
    for h in Assignment.objects.filter(project__course__name=course):
        assigned.append(str(h))
    return text_join(assigned)


def print_projects(course):
    results = []
    for p in Project.objects.filter(course__name=course).order_by('due'):
        results.append('\nProject %s' % p)
        for r in project_requirements(p):
            results.append('    selector=%s, transform=%s' % (r.selector, r.transform))
    return results


def print_data():
    courses = [banner('Courses')] + Course.list()
    bacs200 = [banner('BACS 200'), 'PROJECTS:'] + print_projects('bacs200') + ['', 'LESSONS:'] + Lesson.list('bacs200')
    bacs350 = [banner('BACS 350'), 'PROJECTS:'] + Project.list('bacs350') + ['', 'LESSONS:'] + Lesson.list('bacs350')
    return text_join(courses + bacs200 + bacs350)


def print_students(course):
    students = ['', 'Students in %s' % course]
    for s in Course.students(course):
        u = list_user_login(s.user)
        students.append('%s, %-40s user %s' % (s.pk, s.domain, u))
    return text_join(students)


def project_requirements(project):
    return Requirement.objects.filter(project=project)


def read_schedule(course):
    data_file = 'Documents/unc/%s/schedule.csv' % course
    with open(data_file) as f:
        return [row[:-2] for row in reader(f)]


def schedule_data(course):
    title = Course.objects.get(name=course).title
    return [title, 'Class Schedule'], Lesson.query(course)


def student_data(course):
    return Course.students(course)


def slides_markdown(course, lesson):
    doc = 'Documents/unc/%s/lesson/%s' % (course, lesson)
    text = fix_images(read_markdown(doc), '/static/images/unc/%s' % course)
    bear = '\n\n---\n\n<img src="/static/images/unc/bacs200/Bear.200.png">\n\n---\n\n'
    return bear + text + bear


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
    # print(validate_project_page(dom, course, project))
    return banner('PROJECT %s' % project) + display_test_results(validate_project_page(dom, student, project))


def weekly_agenda(course, week):
    project = Project.lookup(course, week)
    lessons = Lesson.objects.filter(course__name=course, week=week).order_by('date')
    return dict(week=week, lessons=lessons, project=project)


def weekly_lessons(course):
    # weeks = []
    # for w in range(2):
    #     week = w + 1
    #     weekly_agenda(course, week)
    #     # project = Project.lookup(course, week)
    #     # lessons = Lesson.objects.filter(course__name=course, week=week).order_by('date')
    #     weeks.append((lessons, project))
    return [weekly_agenda(course, week+1) for week in range(15)]


def zybooks_link(course, reading):
    match_pattern = r'^(\d+).(\d+) (.*)$'
    url = 'https://learn.zybooks.com/zybook/UNCOBACS%sSeamanFall2019' % course
    replace_pattern = r'<a href="%s/chapter/\1/section/\2">\1.\2 - \3</a>' % url
    link = compile(match_pattern).sub(replace_pattern, reading)
    return link


def add_teacher():
    course_name = 'bacs200'
    name = 'MarkSeaman'
    email = 'mark.b.seaman@gmail.com'
    domain = r'https://unco-bacs.org'
    c = Course.lookup(course_name)
    u = User.objects.get(username=name)
    s = Student.objects.get_or_create(name=name, email=email, course=c, user=u)[0]
    s.user = u
    s.domain = domain
    s.save()

    print(list_users())
    print(print_students(course_name))