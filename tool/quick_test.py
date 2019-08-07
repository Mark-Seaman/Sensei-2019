from unc.bacs import print_data
from tool.log import log, log_exception, log_error
from tool.page import capture_page_features
from tasks.models import Task


def quick_test():
    t = Task.objects.all()[0]
    print('date format'+str(t.date))


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
