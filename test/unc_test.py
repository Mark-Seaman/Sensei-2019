from tool.page import close_browser_dom, open_browser_dom, verify_page
from tool.shell import is_server,text_join
from unc.models import Course, create_course


def unc_views_test():

    if is_server():
        return 'No Selenium on Sensei Server'
    else:
        page = open_browser_dom()

        # url = 'http://unco-bacs.org/bacs200/class/templates/simple.html'
        url = 'https://shrinking-world.com/homework/'
        requirements = ['head', 'body', 'h1', 'title']
        summary = verify_page(page, url, requirements)

        close_browser_dom(page)
        return summary


def unc_data_test():
    create_course('bacs200', 'Web Development Intro (Fall 2019)', 'Mark Seaman',
                  'Web Design and Development for Small Business')
    return text_join([str(c) for c in Course.objects.all()])


def unc_project_test():
    return 'UNC PROJECT - build test'


def unc_lesson_test():
    return 'UNC LESSON - build test'


def unc_review_test():
    return 'UNC REVIEW - build test'


def unc_student_test():
    return 'UNC STUDENT - build test'

