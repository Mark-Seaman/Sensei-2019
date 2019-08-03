from unc.bacs import print_data
from tool.log import log, log_exception, log_page, log_error


def quick_test():
    # Clear the table
    # Lesson.objects.all().delete()

    log_error('Really Bad things happen ')
    log('DATA STRUCTURES: %s' % print_data())
    log('Page Request: %s' % 'https://shrinking-world.com')
    throw_exception()


def throw_exception():
    try:
        open(xxx)
    except:
        log_exception("Failed to open file")
