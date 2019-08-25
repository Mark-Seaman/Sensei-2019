from unc.bacs import *
from unc.projects import *
from test.unc_test import *

'''
DEVELOPMENT SCRIPT

* assign homework
    * display assignments
    * add due date to assignments
    * assign Project #1 to CS350
    * assign Reading #1-3 to CS350
    * assign Project #1 a,b,c and Readings 1-3
    * design Project #1 a,b,c instructions and requirements
    * homework dashboard
'''


def quick_test():
    # x = Student.objects.get(pk=52).delete()
    # x = list_students('bacs350')

    course = 'bacs200'
    # Assignment.objects.all().delete()
    assign_homework(course, '01', '2019-08-30')
    x = list_assignments(course)

    # x = unc_assignment_test()

    # x = import_all_students()

    print(x)


def import_all_students():
    import_students('bacs350')
    import_students('bacs200')
    return unc_student_test()


def delete_students():
    c = create_course('cs350', 'Software Engineering (under development)', 'Mark Seaman',
                  'This class is for test purposes only')
    print(c)
    Student.objects.filter(course=c).delete()


def show_course_content():
    x = list_course_content()
    print(x)


def show_unc_data():

    # Courses
    x = text_join(Course.list())
    x = Course.lookup('cs350')

    # Students
    x = Student.objects.all().delete()
    x = import_test_students()
    x = import_all_students()
    x = unc_student_test()
    x = add_student('Steve Rogers', 'mark.b.seaman+cap@gmail.com', r'https://unco-bacs.org/cap_america', 'cs350')
    x = Student.objects.get('Steve Rogers')
    x = list_users()
    x = list_students('cs350')
    x = [list_students(c) for c in unc_courses()]

    # Projects
    x = import_schedule('cs350')
    x = build_projects('cs350')
    x = unc_project_test()
    x = unc_assignment_test()

    x = list_course_content()

    print(x)

