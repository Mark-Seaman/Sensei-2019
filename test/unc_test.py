from tool.page import close_browser_dom, open_browser_dom #, verify_page
from tool.shell import is_server
from unc.bacs import initialize_data, print_data


def unc_views_test():

    if is_server():
        return 'No Selenium on Sensei Server'
    else:
        page = open_browser_dom()

        # url = 'http://unco-bacs.org/bacs200/class/templates/simple.html'
        url = 'https://shrinking-world.com/homework/'
        requirements = ['head', 'body', 'h1', 'title']
        # summary = verify_page(page, url, requirements)
        summary = "TEST DISABLED"
        close_browser_dom(page)
        return summary


def unc_data_test():
    initialize_data()
    return print_data()


def unc_project_test():
    return 'UNC PROJECT - build test'


def unc_lesson_test():
    return 'UNC LESSON - build test'


def unc_review_test():
    return 'UNC REVIEW - build test'


def unc_student_test():
    return 'UNC STUDENT - build test'

