
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



# def transform_output(text):
#     return text.replace('score','years')


# print('eval: %s' % eval('transform_output("four score")'))


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


