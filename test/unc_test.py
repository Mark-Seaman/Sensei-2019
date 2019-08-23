from tool.shell import is_server
from tool.text import text_lines
from tool.user import list_users
from unc.bacs import *
from unc.projects import build_projects
from unc.models import Student


def unc_views_test():
    if is_server():
        return 'No Selenium on Sensei Server'
    else:
        dom = open_browser_dom()
        student = Student.objects.get(user__username='iron_man')
        summary = validate_unc_project(dom, student, '01')
        summary += validate_unc_project(dom, student, '02')
        summary += validate_unc_project(dom, student, '03')
        close_browser_dom(dom)
        return summary


def unc_data_test():
    initialize_data()
    return "%s lines in output" % len(text_lines(list_course_content()))


def unc_project_test():
    course = 'bacs200'
    return "%s lines in output" % len(build_projects(course))


def unc_lesson_test():
    return zybooks_link('bacs200', '1.1 Web Introduction')


def unc_review_test():
    return 'UNC REVIEW - build test'


def unc_student_test():
    output = ['Sensei Users: ', list_users()]

    for course in ['bacs200', 'bacs350']:
        import_test_students()
        students = list_students(course)
        output.append(students)

        # clear_assignments()
        assign_homework(course, '01')
        assign_homework(course, '02')
        output.append(print_assignments(course))

    return text_join(output)
