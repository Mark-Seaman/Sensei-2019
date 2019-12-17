from django.core.management.base import BaseCommand
from datetime import datetime
from os.path import exists
from os import system
from traceback import format_exc

from tool.days import days_ago, print_recent_dates
from tool.log import log_exception


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('command', nargs='*', type=str)

    def handle(self, *args, **options):
        try:
            if options['command'] and options['command'][0] == 'idea':
                f = 'Documents/info/Index.md'
                with open(f, 'a') as x:
                    x.write('* ' +  ' '.join(options['command'][1:]) + '\n\n')
            elif options['command'] and options['command'][0] == 'days':
                print_recent_dates()
            system('e Documents/info/Index.md Documents/info/Week.md')
            for d in recent_dates():
                edit_task_file(d)
        except:
            log_exception()
            self.stdout.write('** tst Exception (%s) **' % ' '.join(options['command']))
            self.stdout.write(format_exc())


def recent_dates(days=4):
    start = datetime.today()
    return [days_ago(start, days - d - 1) for d in range(days)]


task_default = '''%s

Grow 0

    1, 1, 1, 1
    weight: 20

Teach 0

Tools 0

People 0

Fun 0

'''


def edit_task_file(date):
    f = 'Documents/info/history/%s' % (date.replace ('-', '/'))
    if not exists(f):
        day = datetime.now().strftime("%A")
        open(f, 'w').write(task_default % day)
    system('e %s' % f)

