from tool.text import text_lines
from tool.user import list_users
from unc.bacs import *
from unc.projects import list_projects, import_projects
from unc.skills import print_skills, update_skills


def unc_course_files_test():
    return text_join([show_course_files(course) for course in unc_courses()])


def unc_project_test():
    import_projects('bacs350')
    import_projects('bacs200')
    projects = list_projects('bacs200') + list_projects('bacs350')
    return text_join(projects)  # "%s lines in output" % len(projects)


def unc_lesson_test():
    update_lessons()
    return list_lessons('bacs200') + list_lessons('bacs350')


def unc_review_test():
    return 'UNC REVIEW - build test'


def unc_skills_test():
    update_skills()
    return print_skills('bacs350') + '\n' + print_skills('bacs200')


def unc_student_test():
    output = ['Sensei Users: ', list_users()]

    for course in unc_courses():
        # import_test_students()
        students = list_students(course)
        output.append(students)
    return '%s Student Records' % len(text_lines(text_join(output)))


# def unc_assignment_test():
#     add_test_assignments()
#     return "%s lines in output" % len(text_lines(show_assignments()))

# def unc_data_test():
#     initialize_data()
#     return "%s lines in output" % len(text_lines(list_course_content()))


# def unc_views_test():
#     if is_server():
#         return 'No Selenium on Sensei Server'
#     else:
#         dom = open_browser_dom()
#         student = Student.objects.get(user__username='iron_man')
#         summary = validate_unc_project(dom, student, '01')
#         summary += validate_unc_project(dom, student, '02')
#         summary += validate_unc_project(dom, student, '03')
#         close_browser_dom(dom)
#         return summary
#
#
