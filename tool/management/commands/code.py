from django.core.management.base import BaseCommand
from os import system
import traceback

from tool.code import code_files, code_search, text_search
from tool.log import log_exception
from tool.text import text_join


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
            search(args)
        elif cmd == 'code':
            print('code')
            search_code(args)
        elif cmd == 'files':
            print('files')
            files(args)
        else:
            print('No code command found, ' + cmd)
            code_help()
    else:
        print('No command given')
        code_help()


def code_help():
    print('''
        usage:  dj code cmd [args]

        cmd:
            code  [words]           - Search the code for these words
            files  [component]      - List code files
            search [type] [words]   - Find words in files
            
        ''')


def files(args):
    print("code files %s:" % args)
    print(text_join(code_files(args[0])))


def search(args):
    print("search %s:" % args)
    print(text_search(args))


def search_code(args):
    print("code_search %s:" % args)
    print(code_search(args[0], args[1:]))
