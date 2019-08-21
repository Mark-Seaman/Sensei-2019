from tool.page import close_browser_dom, open_browser_dom
from tool.shell import is_server, text_join
from unc.bacs import import_test_students, assign_homework, initialize_data, print_data, print_students, print_assignments, zybooks_link, validate_unc_project
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
    return print_data()


def unc_project_test():
    course = 'bacs200'
    return text_join(build_projects(course))


def unc_lesson_test():
    return zybooks_link('bacs200', '1.1 Web Introduction')


def unc_review_test():
    return 'UNC REVIEW - build test'


def unc_student_test():
    course = 'bacs200'
    import_test_students()
    students = print_students(course)
    # clear_assignments()
    assign_homework(course, '01')
    assign_homework(course, '02')
    return students + print_assignments()
