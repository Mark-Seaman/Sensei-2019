from unc.models import *


def quick_test():

    course = Course.objects.get(pk=1)
    course.name = 'bacs350'
    course.title = 'Web Development Intermediate (Fall 2019)'
    course.teacher = 'bacs350'
    course.description = 'Intermediate Web Development with PHP/MySQL'
    course.save()

    course = create_course('bacs200', 'Web Development Intro (Fall 2019)', 'Mark Seaman',
                           'Web Design and Development for Small Business')
    print("Course record lookup: ", course)
    for c in Course.objects.all():
        print(c)
