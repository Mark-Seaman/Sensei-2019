from django.core.management.base import BaseCommand
from os import system
import traceback

from tool.log import log_exception


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('script', nargs='+', type=str)

    def handle(self, *args, **options):
        try:
            code_command(self, options['script'])
        except:
            log_exception()
            self.stdout.write('** code Exception (%s) **' % ' '.join(options['script']))
            self.stdout.write(traceback.format_exc())


def code_command(self, options):

    if options:
        cmd = options[0]
        args = options[1:]

        if cmd == 'search':
            print('search')
        elif cmd == 'files':
            print('files')
        else:
            print('No code command found, ' + cmd)
            code_help()
    else:
        print('No command given')
        code_help()


def code_help():
    print('''
        usage:  brain cmd [args]

        cmd:
            search [type] [word]    - Find words in files
            
            files  [component]      - List code files

        ''')