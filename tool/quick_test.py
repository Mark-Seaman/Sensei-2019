from unc.models import *
from unc.bacs import *


def quick_test():
    for l in Lesson.objects.all():
        print(l.topic)


def init_data_test():
    initialize_data()
    print(print_data())


