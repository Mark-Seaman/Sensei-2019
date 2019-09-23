from tool.page import close_browser_dom, open_browser_dom
from tool.shell import is_server
from tool.text import text_lines
from tool.user import list_users
from unc.bacs import *
from unc.projects import add_test_assignments, update_projects, show_assignments, validate_unc_project
from unc.models import Student
from unc.skills import update_skills


def unc_assignment_test():
    add_test_assignments()
    return "%s lines in output" % len(text_lines(show_assignments()))


def unc_course_files_test():
    return text_join([show_course_files(course) for course in unc_courses()])


def unc_sample_files_test():
    return show_sample_files()


def unc_data_test():
    initialize_data()
    return "%s lines in output" % len(text_lines(list_course_content()))


def unc_project_test():
    course = 'cs350'
    output = import_schedule(course)
    update_projects()
    output += list_course_content()
    return "%s lines in output" % len(output)


def unc_lesson_test():
    return zybooks_link('bacs200', '1.1 Web Introduction')


def unc_review_test():
    return 'UNC REVIEW - build test'


def unc_skills_test():
    return update_skills()


def unc_student_test():
    output = ['Sensei Users: ', list_users()]

    for course in unc_courses():
        import_test_students()
        students = list_students(course)
        output.append(students)
    return '%s Student Records' % len(text_lines(text_join(output)))


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


