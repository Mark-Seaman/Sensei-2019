from datetime import datetime
from logging import getLogger
from json import dumps
from traceback import format_exc

from hammer.settings import LOG_FILE
from tool.shell import text_join
from tool.files import read_lines


def log(text, value=None):
    logger = getLogger('hammer')
    if value:
        text = "%s: %s" % (text, value)
    logger.info(str(datetime.now())+',  '+text)


def log_error(message):
    logger = getLogger('hammer')
    message = '\n\n** ERROR ** \n\n%s, %s' % (datetime.now(), message)
    # print(message)
    logger.error(message)


def log_exception(message=''):
    log_error('EXCEPTION OCCURRED: %s\n%s\n\n' % (message, format_exc()))


def log_json(text, data):
    log(text, dumps(data, sort_keys=True, indent=4))


def log_notifications(title, recipients):
    with open('log/notifications.log', 'a') as f:
        text = "%s, %s, %s" % (str(datetime.now()), title, ' '.join(recipients))
        f.write(text+'\n')


def log_page(request, parms=''):
    message = 'PAGE: url=%s%s, user=%s' % (request.get_host(), request.path, request.user.username)
    if parms:
        message += ', %s' % parms
    log(message)


def manage_log_length():
    lines = read_lines(LOG_FILE)
    length = len(lines)
    if length > 5000:
        lines = lines [-1000:]
        open(LOG_FILE, 'w').write('\n'.join(lines))
        return 'Too Long Log - %s, %s lines' % (LOG_FILE, length)
    return 'Log Length OK - %d lines' % length


def recent_log_entries():
    return text_join(read_lines(LOG_FILE)[-100:])

