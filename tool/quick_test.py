from insight.insight import sync_insights
from unc.bacs import *
from unc.dead import update_lessons
from unc.projects import *
from unc.models import *
from unc.review import *
from insight.insight import *


def quick_test():
    import_lessons('bacs350')
    new_350_reviews()

    # assign_team_reviews('bacs200', 'bacs200/nonprofit/index.html', '2019-12-02', bacs200_5_requirements, bacs200_5_notes)

    # sync_insights()
    # print_insights()


def new_350_reviews():
    revs = Review.objects.filter(page='bacs350/slides/index.php')
    print(bacs350_5_requirements)
    for r in revs:
        page = 'bacs350/index.php'
        reviewer, designer = r.reviewer, r.designer
        due = '2019-12-04'
        print('create review: %s,  %s, %s' % (reviewer, designer, due))
        create_review(reviewer.pk, designer.pk, page, due, bacs350_5_requirements, bacs350_5_notes)


def show_course_content():
    x = list_course_content()
    print(x)


# def assign_reviews():
#     show_groups('bacs200')
#     show_groups('bacs350')
#     assign_reviews_round4()
#     # grade_reviews('bacs200/index.html')
#     # grade_reviews('bacs350/index.php')


# def fix_reviews():
#     for r in Review.objects.filter(page='bacs350/superhero.php'):
#         print(r.reviewer.name, r.page)
#         r.page = 'bacs350/superhero/index.php'
#         r.save()
#
#
# def fix_lessons():
#     def change_date(course, lesson, date, week):
#         x = Lesson.lookup(course, lesson)
#         x.date = date
#         x.week = week
#         x.save()
#
#     date = '2019-12-02'
#     change_date('bacs350', 38, date, 14)
#     change_date('bacs200', 36, date, 14)


def init_unc_data():
    x = list_course_content()
    print(x)

    # import_skills('bacs200')
    # import_skills('bacs350')

    # import_lessons('bacs200')
    # import_lessons('bacs350')

    # import_projects('bacs350')
    # import_projects('bacs200')

    # export_skills('bacs200')
    # export_skills('bacs350')

    # export_lessons('bacs200')
    # export_lessons('bacs350')

    # export_projects('bacs350')
    # export_projects('bacs200')

    # Lesson.objects.filter(lesson=-1).delete()
    # init_unc_data()
    # print(print_projects())



