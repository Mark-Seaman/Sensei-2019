from unc.review import print_reviews, assign_reviews
from unc.bacs import *
from unc.projects import *
from unc.models import *
from unc.skills import *

from random import shuffle


def quick_test():
    course = 'bacs200'
#    for s in Course.students(course):
#        print(s.name, s.domain)
    groups = review_groups(course)
    for g in groups:
        print(g)
        
#    assign_reviews()
#    print_reviews()

#    show_reviews_overdue('bacs200')    
#    show_reviews_overdue('bacs350')


def show_reviews_overdue(course):
    print('\nTo Do '+course)
    for r in Review.objects.filter(reviewer__course__name=course, score=-1):
        print("    " + r.reviewer.name)
    print('\nDone '+course)
    for r in Review.objects.filter(reviewer__course__name=course).exclude(score=-1):
        print("    " + r.reviewer.name)

        
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


