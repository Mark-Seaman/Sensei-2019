from unc.bacs import print_data
from tool.log import log, log_exception, log_error
from tool.page import capture_page_features


def quick_test():
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
