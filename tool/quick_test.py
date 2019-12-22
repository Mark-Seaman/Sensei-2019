from insight.insight import *
from insight.models import *
from tool.days import *
from unc.bacs import *
from unc.projects import *
from unc.models import *
from unc.review import *


def quick_test():
    for day in enumerate_month(2019, 4):
        date = datetime.strptime(day, "%Y-%m-%d")
        i = Insight.objects.get_or_create(date=date)[0]
        i.save()
        print(i)


def show_course_content():
    x = list_course_content()
    print(x)


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



