from tool.user import add_user_login, list_users
from unc.bacs import import_test_students, print_students


def quick_test():
    # name, email = 'David Reveles Hernandez', 'reve4760@bears.unco.edu'
    # name, email = 'Tony Stark', 'mark.b.seaman+iron_man@gmail.com'
    # add_user_login(name, email)
    # import_test_students()
    # print(list_users())

    print(print_students('bacs200'))

# def create_bacs_projects():
#     print(text_join(build_projects('bacs200')))
#     approve_requirements(Project.lookup('bacs200', 1))
#     # approve_requirements(Project.lookup('bacs200', 2))



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


