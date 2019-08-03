from django.core.management.base import BaseCommand
import traceback
from re import split

from tool.log import log_exception, recent_log_entries
from tool.text import count_lines, match_pattern, text_lines, text_join
from tool.shell import shell


# ----------------------------------
# Command Interpreter


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('script', nargs='+', type=str)

    def handle(self, *args, **options):
        try:
            system_command(self, options['script'])
        except:
            log_exception()
            self.stdout.write('** tst Exception (%s) **' % ' '.join(options['script']))
            self.stdout.write(traceback.format_exc())


def system_command(self, options):
    '''Execute all of the brain specific brains'''
    # self.stdout.write('starting system command ...')

    if options:
        cmd = options[0]
        args = options[1:]

        if cmd == 'list':
            print(list_processes(args))
        elif cmd == 'log':
            print(recent_log_entries())
        elif cmd == 'procs':
            print(count_processes(args))
        elif cmd == 'prune':
            print(prune_processes(args))
        else:
            print('No system command found, ' + cmd)
            system_help()
    else:
        list_processes()
    # self.stdout.write('... ending  system command')


def system_help():
    print('''
    usage:  system cmd [args]

    cmd:

        list [patterns] - Commit all changes and push
        procs [patterns] - Count the processes that are running
        prune [patterns] - Delete the running processes that are no longer needed

    ''')


def list_processes(args=[]):
    text = shell('ps -ef')
    for pattern in args:
        text = match_pattern(text, pattern)
    return text


def count_processes(args=[]):
    return count_lines(list_processes(args))


def prune_processes(args=[]):
    procs = []
    for p in text_lines(list_processes(args)):
        p = split(' +', p)
        if p[7:]:
            procs.append('kill -9 %-10s # %s' % (p[1], ' '.join(p[7:])[:20]))
    return '\n'.join(procs)
