
from tool.text import text_join
from unc.bacs import approve_requirements, assign_homework, import_students, print_assignments
from unc.models import Project
from unc.projects import build_projects


def quick_test():
    import_students('bacs200')
    # clear_assignments()
    assign_homework('bacs200', '01')
    assign_homework('bacs200', '02')
    print_assignments()


def create_bacs_projects():
    print(text_join(build_projects('bacs200')))
    approve_requirements(Project.lookup('bacs200', 1))
    # approve_requirements(Project.lookup('bacs200', 2))

# from PIL import Image
#     infile = '/Users/seaman/UNC/MarkSeaman/Mark-Seaman-800.jpg'
#     outfile = infile.replace('800', '100')
#     size = 100
#     resize_image(infile, outfile, size)
#
#
# def resize_image(path, newpath, size):
#     print('%s --> %s (%s pixels)' % (path, newpath, size))
#     if path != newpath:
#         try:
#             im = Image.open(path)
#             im.thumbnail((size, size), Image.ANTIALIAS)
#             im.save(newpath, "JPEG")
#         except IOError:
#             print("Cannot resize '%s'" % path)


#
# from tool.page import check_requirements, display_requirements

# from unc.models import Project


#     course, project = 'bacs200', '02'
#     p = Project.lookup(course, project)
#     # approve_requirements(p)
#     check_requirements(p)
#     summary = display_requirements(p)
#     print(summary)
#
#
# def transform_output(text):
#     return text.replace('score','years')


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
