from tool.page import check_requirements, display_requirements

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


from unc.models import Project


def quick_test():
    course, project = 'bacs200', '02'
    p = Project.lookup(course, project)
    # approve_requirements(p)
    check_requirements(p)
    summary = display_requirements(p)
    print(summary)


def transform_output(text):
    return text.replace('score','years')


    # print('eval: %s' % eval('transform_output("four score")'))

# from pprint import PrettyPrinter
# from tool.text import text_join
#
# def requirements_summary(features):
#
#     report = []
#     for i,f in enumerate(features):
#         report.append('\nRequirement #%s - %s:\n\n    %s' % (i+1, f['feature'], f['actual']))
#     return text_join(report)
#
#
# def report_requirements(features):
#     return PrettyPrinter(indent=4, width=200).pformat(features)
#




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
