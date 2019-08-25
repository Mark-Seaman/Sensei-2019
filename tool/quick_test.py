from unc.bacs import *
from unc.bacs import import_all_students
from unc.projects import *
from test.unc_test import *
from unc.projects import assign_project_1, show_assignments

'''
DEVELOPMENT SCRIPT

* student login
    * learn from S1 code
    * design UNC BACS login form
    * redirect to login
    * logout
    * student login status
    * improve login sequence for students
    * anonymous access
    
'''


def quick_test():
    assign_project_1()
    x = show_assignments()
    print(x)


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

