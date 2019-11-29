from _csv import reader
from random import shuffle
from django.views.generic import TemplateView, UpdateView

from tool.days import due_date, date_str
from tool.text import text_join
from unc.bacs import zybooks_link, list_students, unc_courses, add_student, read_schedule, add_lesson
from unc.models import Student, Lesson, Project, Assignment, Course, Review
from unc.review import student_reviews_done, student_reviews


# --------------------------------
#       D E A D   C O D E
# --------------------------------

class UncReviews(TemplateView):
    template_name = 'unc_reviews.html'

    def get_context_data(self, **kwargs):
        course = '1'
        reviews = query_reviewers(course)
        designers = query_designers(course)
        return site_settings(student_active='active', title='Design Reviews', reviews=reviews, designers=designers)


class UncStudentEdit(UpdateView):
    model = Student
    fields = ['domain']
    template_name = 'unc_student.html'
    success_url = '/unc/bacs200'

    def get_context_data(self, **kwargs):
        log_page(self.request)
        kwargs = super(UncStudent, self).get_context_data(**kwargs)
        header = 'UNC Student Profile', kwargs[
            'object'].name, "/static/images/unc/Bear.200.png", 'UNC Bear', '/unc/bacs200'
        kwargs['header'] = dict(title=header[0], subtitle=header[1], logo=header[2], logo_text=header[3],
                                href=header[4])
        return kwargs


def get_lesson(course, lesson_num):
    return Lesson.lookup(course, lesson_num)


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
    set_lesson_topic(course, '34', 'Teamwork', '9.1 Mobile websites (optional)')
    set_lesson_topic(course, '35', 'Contribution', '9.2 Mobile tools (optional)')
    set_lesson_topic(course, '36', 'Project Management', '')

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
    set_lesson_topic(course, '34', 'Technical Debt', '9.6 Ajax')
    set_lesson_topic(course, '35', 'Requirements', '9.8 Weather App')
    set_lesson_topic(course, '36', 'User Authentication', '9.9 Currency')
    set_lesson_topic(course, '37', 'Design', '')
    set_lesson_topic(course, '38', 'Code', '')


def list_projects(course):
    results = []
    for p in Project.objects.filter(course__name=course).order_by('due'):
        results.append('\nProject %s' % p)
        for r in p.requirements:
            results.append('    selector=%s, transform=%s' % (r.selector, r.transform))
    return text_join(results)


def update_projects():
    course = 'bacs200'
    create_project(course, '01', 'index.php')
    create_project(course, '02', 'bacs200/inspire.html')
    create_project(course, '03', 'bacs200/amuse.html')
    create_project(course, '04', 'bacs200/project/index.html')
    create_project(course, '05', 'bacs200/study_guide.html')
    create_project(course, '06', 'bacs200/index.html')
    create_project(course, '07', 'bacs200/wanted.html')
    create_project(course, '08', 'bacs200/learn.html')
    create_project(course, '09', 'bacs200/teach.html')
    create_project(course, '10', 'bacs200/index.html')
    create_project(course, '11', 'bacs200/travel/index.html')
    create_project(course, '12', 'docs/ProjectPlan.md')
    create_project(course, '13', 'bacs200/nonprofit/index.html')

    course = 'bacs350'
    create_project(course, '01', 'index.php')
    create_project(course, '02', 'bacs350/index.php')
    create_project(course, '03', 'bacs350/superhero/index.php')
    create_project(course, '04', 'bacs350/planner/index.php')
    create_project(course, '05', 'bacs350/docman/index.php')
    create_project(course, '06', 'bacs350/subscriber/index.php')
    create_project(course, '07', 'bacs350/superhero/index.php')
    create_project(course, '08', 'bacs350/notes/index.php')
    create_project(course, '09', 'bacs350/review/index.php')
    create_project(course, '10', 'bacs350/review/index.php')
    create_project(course, '11', 'bacs350/slides/index.php')
    create_project(course, '12', 'bacs350/index.php')
    create_project(course, '13', 'bacs350/index.php')
    create_project(course, '14', 'bacs350/index.php')


def list_assignments(course):
    assigned = ['\n\nAssignments for %s:           project          due            status         last update\n' % course]
    for h in Assignment.objects.filter(project__course__name=course):
        assigned.append(str(h))
    return text_join(assigned)


def show_assignments():
    return text_join([list_assignments(c) for c in Course.all()])


def test_project_page(student, project):
    if student:
        dom = open_browser_dom()
        data = validate_project_page(dom, student, project)
        close_browser_dom(dom)
        return data


def add_requirement(project, id, selector, transform):
    r = Requirement.objects.get_or_create(project=project, selector=selector)[0]
    r.num = id
    r.label = selector
    r.transform = transform
    r.save()
    return r


def approve_requirements(course, id):
    project = Project.lookup(course, id)
    for i, r in enumerate(project.requirements):
        r.correct = r.actual
        r.save()


def validate_project_page(dom, student, project):
    p = Project.lookup(student.course.name, project)
    url = join(student.domain, p.page)
    source = capture_page(dom, url)
    requirements = capture_page_features(dom, p.requirements)
    student = 'Mark Seaman'
    return dict(student=student, url=url, requirements=requirements, source=source, date=now())


def validate_unc_project(dom, student, project):
    return banner('PROJECT %s' % project) + display_test_results(validate_project_page(dom, student, project))


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


def assign_homework(course, project, due):
    for s in Course.students(course):
        add_assignment(course, s, project, due)


def build_projects(course):
    create_project_record(course, '01', 'index.php', fake_project_requirements())
    create_project_record(course, '02', 'bacs350/index.html', fake_project_requirements())
    # create_project_record(course, '03', 'bacs350/profile.html', bacs200_project1_requirements())
    return list_project_details(course)


def clear_assignments():
    Assignment.objects.all().delete()


def add_test_assignments():
    course = 'cs350'
    assign_homework(course, '01', '2019-08-30')
    assign_homework(course, '02', '2019-09-06')
    # clear_assignments()


def fix_domains():
    for s in Student.objects.filter():
        if s.domain != 'No Domain Configured':
            if not s.domain.startswith('http'):
                s.domain = 'http://'+s.domain
                s.save()
                print(s.domain)


def add_project(course, row):
    date = make_aware(parse_date(row[2]))
    date = date_str(date)
    page = '%s/project/%s' % (course, row[0])
    instructions = '/unc/%s/project/%s' % (course, row[0])
    title = row[6] if row[6:] else 'None'
    return create_project(course, row[0], title, page, date, instructions)


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


def query_reviewers(course):

    def reviewer_summary(student):
        student_id = student.pk
        reviews = student_reviews_done(student_id)
        not_done = student_reviews(student_id)
        assigned = len(reviews) + len(not_done)
        rounds = 13
        points = 10 * rounds * len(reviews) / assigned
        return student, reviews, "%d done of %d assigned, score = %d" % (len(reviews), assigned, points)

    all_students = Course.students(course)
    return [reviewer_summary(s) for s in all_students]


def query_designers(course):

    def designer_summary(student):
        student_id = student.pk
        reviews = review_feedback(student_id).filter(page='bacs200/projects/nonprofit.html')
        scores = ','.join([str(r.score) for r in reviews if r.page=='bacs200/projects/nonprofit.html'])
        return student, reviews, "%d reviews, scores: %s" % (len(reviews), scores)

    all_students = Course.students(course)
    return [designer_summary(s) for s in all_students]


def projects():
    return len(Review.objects.all().distinct('due'))


def review_groups(course):

    groups = []
    num = 8
    s = Course.students(course)
    shuffle(s)
    x = 0
    while s[x:x + num]:
        groups.append(s[x:x + num])
        x += num
    # groups = [groups[0] + groups[-1]] + groups[1:-1]
    return groups


def review_pairs(groups):
    x = []
    for team in groups:
        for reviewer in team:
            for designer in team:
                if reviewer != designer:
                    x.append((designer, reviewer))
    print(len(x))
    return x


def url_feedback(answer, correct):
    if answer == correct:
        return 'smiley1.jpg'
    else:
        return 'sad1.jpg'


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