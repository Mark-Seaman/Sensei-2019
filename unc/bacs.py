from csv import reader
from django.utils.timezone import make_aware
from re import compile

from tool.days import parse_date
from tool.document import fix_images, read_markdown
from tool.files import recursive_list
from tool.log import log_exception
from tool.shell import banner
from tool.text import text_join
from tool.user import add_user_login
from unc.models import Course, Project, Lesson, Skill, Student
from unc.projects import add_project, list_assignments


def add_lesson(course, row):
    # CSV Data -- Week, Day, Date, Lesson, Topic, Reading, Projects, Process, Parts
    # print(row)
    project = add_project(course, row)
    date = make_aware(parse_date(row[2]))
    num = row[3] if row[3] != '' else '-1'
    x = Lesson.objects.filter(course=project.course, date=date)
    if len(x)> 1:
        print (x)
    lesson = Lesson.objects.get_or_create(course=project.course, date=date)[0]
    lesson.week = row[0]
    lesson.lesson = num
    lesson.project = project
    lesson.topic = row[4]
    lesson.reading = zybooks_link(course[-3:], row[5])
    lesson.save()
    return lesson


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


def import_all_students():
    import_students('bacs350')
    import_students('bacs200')
    print(text_join([list_students(c) for c in unc_courses()]))


def import_students(course):
    def read_students(course):
        data_file = 'Documents/unc/%s/students.csv' % course
        with open(data_file) as f:
            return [row for row in reader(f)]

    def display_student(course, first, last, email):
        print('%s, "%s_%s", %s' % (course, first, last, email))

    table = read_students(course)
    if course == 'bacs200':
        for row in table[2:]:
            # print(row)
            name = row[0].split(' ')
            first, last, email = name[0], ' '.join(name[1:]), row[3]
            display_student(course, first, last, email)
            add_student(first, last, email, 'No Domain Configured', course)
    else:
        for row in table[2:-1]:
            # print(row)
            name = row[0].split(' ')
            first, last, email = name[0], ' '.join(name[1:]), row[3]
            display_student(course, first, last, email)
            add_student(first, last, email, 'No Domain Configured', course)


def import_schedule(course):
    table = read_schedule(course)
    for row in table[2:]:
        add_lesson(course, row)
    return text_join(Lesson.list(course))


# def import_test_students():
#     course = 'cs350'
#     add_student('Tony', 'Stark', 'mark.b.seaman+iron_man@gmail.com', r'https://unco-bacs.org/iron_man', course)
#     add_student('Natasha', 'Romanov ', 'mark.b.seaman+black_widow@gmail.com', r'https://unco-bacs.org/black_widow',
#                 course)
#     add_student('Bruce', 'Banner', 'mark.b.seaman+hulk@gmail.com', r'https://unco-bacs.org/hulk', course)
#     add_student('Steve', 'Rogers', 'mark.b.seaman+cap@gmail.com', r'https://unco-bacs.org/cap_america', course)
#     add_student('Carol', 'Danvers', 'mark.b.seaman+marvel@gmail.com', r'https://unco-bacs.org/cap_marvel', course)
#     add_student('Wanda', 'Maximoff', 'mark.b.seaman+witch@gmail.com', r'https://unco-bacs.org/scarlet_witch', course)
#     add_student('Sensei', '200', 'mark.b.seaman+200@gmail.com', r'https://unco-bacs.org', 'bacs200')
#     add_student('Sensei', '350', 'mark.b.seaman+350@gmail.com', r'https://unco-bacs.org', 'bacs350')
#

def list_course_content():
    data = [banner('Course Content Data')]
    data += Course.list()
    for c in unc_courses():
        data.append(banner(c))
        data.append('\nPROJECTS:\n')
        data += Project.list(c)
        data.append('\nLESSONS:\n')
        data += Lesson.list(c)
        data.append('\nSTUDENTS:')
        data.append(list_students(c))
        data.append('\nASSIGNMENTS:')
        data.append(list_assignments(c))
    return text_join(data)


def list_lessons(course):
    return text_join(Lesson.list(course))


def list_students(course):
    return ("\nStudents %s:\n" % course) + text_join([str(s) for s in Course.students(course)])


def read_schedule(course):
    data_file = 'Documents/unc/%s/schedule.csv' % course
    with open(data_file) as f:
        return [row[:-2] for row in reader(f)]


def schedule_data(course):
    title = Course.objects.get(name=course).title
    return [title, 'Class Schedule'], Lesson.query(course)


def slides_markdown(course, lesson):
    doc = 'Documents/unc/%s/lesson/%s' % (course, lesson)
    text = fix_images(read_markdown(doc), '/static/images/unc/%s' % course)
    bear = '\n\n---\n\n<img src="/static/images/unc/bacs200/Bear.200.png">\n\n---\n\n'
    return bear + text + bear


def student_data(course):
    return Course.students(course)


def student_projects(course):
    skills = [s.images.split(',')[0] for s in Skill.query(course)[5:]]
    projects = Project.query(course)[5:10]
    return [(s, projects, skills) for s in Course.students(course)]


def show_course_files(course):
    return banner(course) + text_join(recursive_list('Documents/unc/%s' % course))


def unc_courses():
    return Course.all()


def update_lessons():

    def set_lesson_topic(course, lesson_id, name, zybooks=None):
        x = Lesson.lookup(course, lesson_id)
        x.topic = name
        if zybooks:
            x.reading = zybooks_link(course[-3:], zybooks)
        x.save()

    course = 'bacs200'
    set_lesson_topic(course, '11', 'Forming URLs')
    set_lesson_topic(course, '12', 'Development Workflow')
    set_lesson_topic(course, '13', 'Test and Debug')
    set_lesson_topic(course, '14', 'Using Stylesheets')
    set_lesson_topic(course, '15', 'Text & Color')
    set_lesson_topic(course, '16', 'Spacing & Borders')
    set_lesson_topic(course, '17', 'Page Layout')
    set_lesson_topic(course, '18', 'Page Structure')
    set_lesson_topic(course, '19', 'Menus', '4.5 Font & Text Properties')
    set_lesson_topic(course, '20', 'Bootstrap', '4.6 Box Model')
    set_lesson_topic(course, '21', 'Tab View', '3.1 HTML Containers')
    set_lesson_topic(course, '22', 'Accordion', '3.2 Forms')
    set_lesson_topic(course, '23', 'Version Control', '3.3 Common Widgets')
    set_lesson_topic(course, '24', 'W3Schools', '3.4 HTML5 Widgets')
    set_lesson_topic(course, '25', 'W3Schools Tutorials', '3.5 Audio & Video')
    set_lesson_topic(course, '26', 'Photoshop', '3.6 Script and Style')
    set_lesson_topic(course, '27', 'Illustrator', '3.7 HTML Developer Guidelines')
    set_lesson_topic(course, '28', 'Website Usability', '3.8 Restaurant Reviews')
    set_lesson_topic(course, '29', 'Design', '3.9 Lab Practice')
    set_lesson_topic(course, '30', 'Brackets Extensions', '2.9 Band Page')
    set_lesson_topic(course, '31', 'Design Diagrams', '2.10 - News Article Lab')
    set_lesson_topic(course, '32', 'Project Planning', '4.7 - Band Example')
    set_lesson_topic(course, '33', 'Learning', '4.8 - News Article Lab')

    course = 'bacs350'
    set_lesson_topic(course, '11', 'Document Viewer')
    set_lesson_topic(course, '12', 'Document Manager')
    set_lesson_topic(course, '13', 'Directory Listing')
    set_lesson_topic(course, '14', 'Document Select')
    set_lesson_topic(course, '15', 'SQL Tables')
    set_lesson_topic(course, '16', 'Database Connect')
    set_lesson_topic(course, '17', 'List Rows ')
    set_lesson_topic(course, '18', 'CRUD Operations')
    set_lesson_topic(course, '19', 'Add Records')
    set_lesson_topic(course, '20', 'Update Records')
    set_lesson_topic(course, '21', 'Data Form Views', '14.1 Relational Databases')
    set_lesson_topic(course, '22', 'Edit View', '14.2 SQL')
    set_lesson_topic(course, '23', 'Forms App', '14.3 Tables')
    set_lesson_topic(course, '24', 'Logging', '14.4 Insert Records')
    set_lesson_topic(course, '25', 'Review Manager App', '14.5 Selecting Records')
    set_lesson_topic(course, '26', 'Design Reviews', '14.6 SQL Functions')
    set_lesson_topic(course, '27', 'Page Caching', '14.7 Joining Tables')
    set_lesson_topic(course, '28', 'Page Template', '14.8 Modifying Rows')
    set_lesson_topic(course, '29', 'Component Templates', '9.1 jQuery')
    set_lesson_topic(course, '30', 'MVC Design Pattern', '9.2 Selectors')
    set_lesson_topic(course, '31', 'Reveal JS', '9.3 Events')
    set_lesson_topic(course, '32', 'Slide Show App', '9.4 Styles')
    set_lesson_topic(course, '33', 'Documentation', '9.5 DOM')
    set_lesson_topic(course, '34', 'Code Reuse', '9.6 Ajax')
    set_lesson_topic(course, '35', 'Users', '9.7 Plugins')



def weekly_agenda(course, week):
    project = Project.lookup(course, week)
    lessons = Lesson.objects.filter(course__name=course, week=week).order_by('date')
    return dict(week=week, lessons=lessons, project=project)


def weekly_lessons(course):
    return [weekly_agenda(course, week + 1) for week in range(12)]


def zybooks_link(course, reading):
    match_pattern = r'^(\d+).(\d+) (.*)$'
    url = 'https://learn.zybooks.com/zybook/UNCOBACS%sSeamanFall2019' % course
    replace_pattern = r'<a href="%s/chapter/\1/section/\2">\1.\2 - \3</a>' % url
    link = compile(match_pattern).sub(replace_pattern, reading)
    return link


