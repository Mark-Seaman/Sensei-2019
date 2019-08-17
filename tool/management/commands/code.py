from django.core.management.base import BaseCommand
from traceback import format_exc
from os import system

from tool.code import code_files, list_functions, source_code, text_search
from tool.log import log_exception
from tool.text import text_join, text_lines


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('script', nargs='+', type=str)

    def handle(self, *args, **options):
        try:
            code_command(options['script'])
        except:
            log_exception()
            self.stdout.write('** code Exception (%s) **' % ' '.join(options['script']))
            self.stdout.write(format_exc())


def code_command(options):

    if options:
        cmd = options[0]
        args = options[1:]

        if cmd == 'search':
            print(text_search(args))
        elif cmd == 'functions':
            functions()
        elif cmd == 'files':
            files(args)
        elif cmd == 'migrate':
            migrate_database()
        elif cmd == 'source':
            source()
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
            functions               - List all the functions
            search [type] [words]   - Find words in files
            
        ''')


def execute_command(command):
    code_command(command.split(' '))


def files(path):
    if not path:
         path = ['.']
    print("code files %s:" % path[0])
    print(text_join(code_files(path[0])))


def functions():
    print('code functions:')
    print(list_functions())


def migrate_database():
    system('python manage.py makemigrations && python manage.py migrate')


def source():
    print('source code:')
    source_text = source_code()
    print('%s files, %s lines of source code' % (len(code_files()), len(text_lines(source_text))))

