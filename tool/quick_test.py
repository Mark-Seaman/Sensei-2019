from unc.review import print_reviews, assign_reviews
from unc.bacs import *
from unc.projects import *
from unc.models import *
from unc.skills import *


def quick_test():
    assign_reviews()
    # reviewer = Student.lookup('Sensei 200')
    print_reviews()


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


