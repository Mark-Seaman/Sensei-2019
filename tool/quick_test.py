from insight.insight import sync_insights
from unc.bacs import *
from unc.dead import update_lessons
from unc.projects import *
from unc.models import *
from unc.review import *
from insight.insight import *
from insight.models import *
from tool.days import date_str


def quick_test():
    # print('\n'.join(enumerate_month(2019, 10)))
    # print('\n'.join(enumerate_month(2019, 11)))
    # print('\n'.join(enumerate_month(2019, 12)))
    for i in Insight.objects.all():
        i.day = date_str(i.date)
        i.save()
        print(i.pk, i.day, i.topic, i.name)


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



