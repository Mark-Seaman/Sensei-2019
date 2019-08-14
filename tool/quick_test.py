from unc.bacs import build_projects
from tool.page import validate_project_page

'''
Development To Do:

Page Tester
    Transform structure
        add requirement.transform
        debug eval logic
    Tranform functions
        text ()
        search (regex)
        replace (regex, sub)
        lines (min, max)
        chars (min, max)
        links ()
    Page Test
        get page
        capture features
        verify requirements
        present feedback
        approve requirements
        automated test
        interactive test view
        rerun test
'''

from tool.page import close_browser_dom, open_browser_dom, validate_project_page


def quick_test():
    page = open_browser_dom()
    summary = validate_project_page('bacs200', '02')
    close_browser_dom(page)
    display_test_results(summary)

    # print('eval: %s' % eval('transform_output("four score")'))


def display_test_results(data):
    print('Student: %s' % data['student'])
    print('URL: %s' % data['url'])
    for i,r in enumerate(data['requirements']):
        r.num = i+1
        r.save()
        print('Requirement: %s, %s, %s' % (r.num, r.selector, r.actual))


def transform_output(text):
    return text.replace('score','years')








# from tool.log import log, log_exception, log_error
# from tool.page import capture_page_features
# from tasks.models import Task

# def task_dates():
#     t = Task.objects.all()[0]
#     print('date format' + str(t.date))


# def read_schedule():
#     import_schedule('bacs350')
#     # print(print_data())


# def capture_page():
#     print(capture_page_features('https://shrinking-world.com/unc/bacs200/schedule',
#                                 ['head', 'body', 'title', 'h1']))


# def test_log_feature():
#     log_error('Really Bad things happen ')
#     log('DATA STRUCTURES: %s' % print_data())
#     log('Page Request: %s' % 'https://shrinking-world.com')
#     throw_exception()
#
#
# def throw_exception():
#     try:
#         open('xxx')
#     except:
#         log_exception("Failed to open file")
