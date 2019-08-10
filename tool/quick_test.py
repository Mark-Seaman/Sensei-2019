from unc.bacs import import_schedule, print_data
from tool.log import log, log_exception, log_error
from tool.page import capture_page_features
from tasks.models import Task
from re import compile


def quick_test():
    read_schedule()


def zybooks_link():
    match_pattern = r'^(\d).(\d) (.*)$'
    replace_pattern = r'<a href="https://learn.zybooks.com/zybook/UNCOBACS200SeamanFall2019/chapter/\1/section/\2">\1.\2 - \3</a>'
    text = '1.7 Intro to JavaScript'
    text = compile(match_pattern).sub(replace_pattern, text)
    print(text)


def task_dates():
    t = Task.objects.all()[0]
    print('date format' + str(t.date))


def read_schedule():
    # import_schedule('bacs200')
    print(print_data())


def capture_page():
    print(capture_page_features('https://shrinking-world.com/unc/bacs200/schedule',
                                ['head', 'body', 'title', 'h1']))


def test_log_feature():
    log_error('Really Bad things happen ')
    log('DATA STRUCTURES: %s' % print_data())
    log('Page Request: %s' % 'https://shrinking-world.com')
    throw_exception()


def throw_exception():
    try:
        open(xxx)
    except:
        log_exception("Failed to open file")
