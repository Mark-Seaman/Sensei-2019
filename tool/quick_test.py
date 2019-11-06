from unc.bacs import *
from unc.projects import *
from unc.models import *
from unc.review import *
from unc.skills import *


def quick_test():
    init_unc_data()
    # fix_reviews()

    # grade_reviews('bacs200/index.html')
    # grade_reviews('bacs350/index.php')

    # show_groups('bacs200')
    # show_groups('bacs350')
    # assign_reviews_round3()


def fix_reviews():
    for r in Review.objects.filter(page='bacs350/superhero.php'):
        print(r.reviewer.name, r.page)
        r.page = 'bacs350/superhero/index.php'
        r.save()


def init_unc_data():
    # x = import_schedule('bacs200')
    # x = import_schedule('bacs350')
    update_lessons()
    update_projects()
    update_skills()
    # x = list_course_content()
    # print(x)


def show_course_content():
    x = list_course_content()
    print(x)


