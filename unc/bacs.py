from csv import reader
from re import compile

from tool.days import date_str, due_date
from tool.document import fix_images, read_markdown
from tool.files import recursive_list
from tool.log import log_exception
from tool.shell import banner
from tool.text import as_text, text_join
from tool.user import add_user_login
from unc.models import Course, Project, Lesson, Skill, Student


def add_student(first, last, email, domain, course):
    course = Course.lookup(course)
    name = '%s %s' % (first, last)
    s = Student.objects.get_or_create(name=name, email=email, course=course)[0]
    u = add_user_login(first, last, email)
    s.user = u
    s.domain = domain
    s.save()
    return s


def get_student(request):
    try:
        if not request.user.is_anonymous:
            return Student.objects.get(user=request.user)
    except:
        log_exception('Cannot find student record, %s' % str(request.user))


def list_course_content():
    data = [banner('Course Content Data')]
    data += Course.list()
    for c in unc_courses():
        data.append(banner(c))
        data.append('\nPROJECTS:\n')
        data += [str(p) for p in Project.list(c)]
        data.append('\nLESSONS:\n')
        data += Lesson.list(c)
        data.append('\nSTUDENTS:')
        data.append(list_students(c))
        # data.append('\nASSIGNMENTS:')
        # data.append(list_assignments(c))
    return text_join(data)


def list_lessons(course):
    return as_text(Lesson.list(course))


def lessons_csv(course):
    return 'Documents/unc/%s/lessons.csv' % course


def add_lesson(course, lesson_num, topic, week, date, reading):
    lesson = Lesson.lookup(course, lesson_num)
    lesson.topic = topic
    lesson.week = week
    lesson.date = due_date(date)
    lesson.reading = reading
    lesson.zybooks = zybooks_link(course[-3:], reading)
    lesson.save()
    return lesson


def export_lessons(course):
    with open(lessons_csv(course), 'w') as f:
        for x in Lesson.list(course):
            text = ','.join([course, str(x.lesson), x.topic, str(x.week), date_str(x.date), x.reading])
            f.write("%s\n" % text)


def import_lessons(course):
    Lesson.objects.filter(course__name=course).delete()
    with open(lessons_csv(course)) as f:
        for row in reader(f):
            if len(row) > 5:
                add_lesson(row[0], row[1], row[2], row[3], row[4], row[5])


def list_students(course):
    return ("\nStudents %s:\n" % course) + text_join([str(s) for s in Course.students(course)])


def read_schedule(course):
    data_file = 'Documents/unc/%s/schedule.csv' % course
    with open(data_file) as f:
        return [row[:-2] for row in reader(f)]


def schedule_data(course):
    title = Course.objects.get(name=course).title
    return [title, 'Class Schedule'], Lesson.list(course)


def slides_markdown(course, lesson):
    doc = 'Documents/unc/%s/lesson/%s' % (course, lesson)
    text = fix_images(read_markdown(doc), '/static/images/unc/%s' % course)
    bear = '\n\n---\n\n<img src="/static/images/unc/bacs200/Bear.200.png">\n\n---\n\n'
    return bear + text + bear


def slides_django_markdown(lesson):
    doc = 'Documents/unc/django/%s.md' % lesson
    text = fix_images(read_markdown(doc), '/static/images/unc/django')
    bear = '\n\n---\n\n<img src="/static/images/unc/bacs200/Bear.200.png">\n\n---\n\n'
    return bear + text + bear


def student_data(course):
    return Course.students(course)


def student_projects(course):
    skills = [s.images.split(',')[0] for s in Skill.list(course)[5:]]
    projects = Project.list(course)[5:10]
    return [(s, projects, skills) for s in Course.students(course)]


def show_course_files(course):
    return banner(course) + text_join(recursive_list('Documents/unc/%s' % course))


def unc_courses():
    return Course.all()


def weekly_agenda(course, week):
    project = Project.lookup(course, week)
    lessons = Lesson.objects.filter(course__name=course, week=week).order_by('date')
    return dict(week=week, lessons=lessons, project=project)


def weekly_lessons(course):
    weeks = 14
    return [weekly_agenda(course, week + 1) for week in range(weeks)]


def zybooks_link(course, reading):
    if reading:
        match_pattern = r'^(\d+).(\d+) (.*)$'
        url = 'https://learn.zybooks.com/zybook/UNCOBACS%sSeamanFall2019' % course
        replace_pattern = r'<a href="%s/chapter/\1/section/\2">\1.\2 - \3</a>' % url
        link = compile(match_pattern).sub(replace_pattern, reading)
        return link

