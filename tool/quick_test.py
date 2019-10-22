from test.unc_test import *
from unc.bacs import *
from unc.projects import *
from unc.models import *
from unc.skills import *
from tasks.summary import *


def quick_test():
    init_unc_data()


def init_unc_data():
    # x = import_schedule('bacs200')
    # x = import_schedule('bacs350')
    update_topics()
    update_projects()
    update_skills()
    x = list_course_content()
    print(x)


def show_course_content():
    x = list_course_content()
    print(x)


