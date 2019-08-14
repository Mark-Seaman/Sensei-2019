from tool.page import close_browser_dom, open_browser_dom, validate_project_page
from tool.shell import banner, is_server, text_join
from unc.bacs import build_projects, initialize_data, print_data, print_projects, zybooks_link


def unc_views_test():

    if is_server():
        return 'No Selenium on Sensei Server'
    else:
        page = open_browser_dom()
        summary = banner('PROJECT 01') + display_test_results(validate_project_page('bacs200', '01'))
        summary += banner('PROJECT 02') + display_test_results(validate_project_page('bacs200', '02'))
        summary += banner('PROJECT 03') + display_test_results(validate_project_page('bacs200', '03'))
        close_browser_dom(page)
        return summary

    # print('eval: %s' % eval('transform_output("four score")'))


def display_test_results(data):
    results = []
    results.append('Student: %s' % data['student'])
    results.append('URL: %s' % data['url'])
    for i,r in enumerate(data['requirements']):
        r.num = i+1
        r.save()
        results.append('Requirement: %s, %s, %s' % (r.num, r.selector, r.actual))
    return text_join(results)


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


