from csv import reader

from tool.days import due_date, date_str
from tool.text import as_text
from unc.dead import add_project
from unc.models import Assignment, Lesson, Project


def add_project(course, num, title=None, page=None, due=None):
    project = Project.lookup(course, num)
    project.title = "Project #%s" % num
    if title:
        project.title += ' - ' + title
    if page:
        project.page = page
    if due:
        project.due = due_date(due)
    project.instructions = '/unc/%s/project/%s' % (course, num)
    project.save()
    return project


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



def list_projects(course):
    return as_text(Project.list(course))


def project_csv(course):
    return 'Documents/unc/%s/projects.csv' % course


def import_projects(course):
    with open(project_csv(course)) as f:
        for row in reader(f):
            if len(row) > 4:
                add_project(row[0], row[1], row[2], row[3], row[4])


def export_projects(course):
    with open(project_csv(course), 'w') as f:
        for project in Project.list(course):
            f.write("%s,%s,%s,%s,%s\n" % (course, project.num, project.title, project.page, date_str(project.due)))


def print_projects():
    for course in ['bacs200', 'bacs350']:
        print("\n%s" % c)
        for p in Project.list(course):
            print("    [%d] %s - due %s - %s" % (p.pk, p.title, date_str(p.due), p.page))



