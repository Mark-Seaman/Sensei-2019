from unc.review import print_reviews, assign_reviews
from unc.bacs import *
from unc.projects import *
from unc.models import *
from unc.skills import *


def quick_test():
#    assign_reviews()
    # reviewer = Student.lookup('Sensei 200')
#    print_reviews()
    reviews_overdue()

def reviews_overdue():
    course = 'bacs200'
    print('\nTo Do '+course)
    for r in Review.objects.filter(reviewer__course__name=course, score=-1):
        print(r.reviewer.name)
    print('\nDone '+course)
    for r in Review.objects.filter(reviewer__course__name=course).exclude(score=-1):
        print(r.reviewer.name)

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


