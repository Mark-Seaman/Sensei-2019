from tool.page import close_browser_dom, open_browser_dom, validate_project_page, display_test_results
from tool.shell import banner, is_server, text_join
from unc.bacs import build_projects, initialize_data, print_data, print_projects, zybooks_link


def validate_unc_project(dom, course, project, ):
    return banner('PROJECT %s' % project) + display_test_results(validate_project_page(dom, course, project))


def unc_views_test():
    if is_server():
        return 'No Selenium on Sensei Server'
    else:
        dom = open_browser_dom()
        summary = validate_unc_project(dom, 'bacs200', '01')
        summary += validate_unc_project(dom, 'bacs200', '02')
        summary += validate_unc_project(dom, 'bacs200', '03')
        close_browser_dom(dom)
        return summary


def unc_data_test():
    initialize_data()
    return print_data()


def unc_project_test():
    course = 'bacs200'
    build_projects(course)
    return text_join(print_projects(course))


def unc_lesson_test():
    return zybooks_link('bacs200', '1.1 Web Introduction')


def unc_review_test():
    return 'UNC REVIEW - build test'


def unc_student_test():
    return 'UNC STUDENT - build test'


