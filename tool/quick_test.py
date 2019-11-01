from unc.bacs import *
from unc.projects import *
from unc.models import *
from unc.review import *
from unc.skills import *


def quick_test():
    update_projects()
    # init_unc_data()
    # grade_reviews('bacs200/index.html')

    # show_groups('bacs200')
    # show_groups('bacs350')
    # assign_reviews_round2()

    # create_project(course, num, title, page, due, instructions)



def create_project(course, num, title, page, due, instructions):
    course = Course.objects.get(name=course)
    due = due_date(due)
    project = Project.objects.get_or_create(course=course, num=num)[0]
    project.title = title
    project.page = page
    project.due = due
    project.instructions = instructions


def init_unc_data():
    # x = import_schedule('bacs200')
    # x = import_schedule('bacs350')
    update_lessons()
    update_projects()
    update_skills()
    x = list_course_content()
    print(x)


def show_course_content():
    x = list_course_content()
    print(x)


