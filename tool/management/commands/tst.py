from django.core.management.base import BaseCommand
from inspect import getmembers, isfunction
from os import listdir, system
from traceback import format_exc

from hammer.settings import TEST_DIR
from tool.log import log_exception
from tool.models import Test
from tool.shell import differences, banner


def quick_test():
     system('cd $p && python manage.py code search tool def')
     # system('cd $p && python manage.py code files tool')

    # Other Quick Tests
    # from test.text_test import text_html_search_test
    # print(text_html_search_test())
    # from test.text_test import text_doc_search_test
    # print(text_doc_search_test())
    # from test.task_test import task_days_age_test
    # print(task_days_age_test())


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('command', nargs='*', type=str)

    def handle(self, *args, **options):
        try:
            # print('OPTIONS %s' % options['command'])
            tst_command(self, options['command'])
        except:
            log_exception()
            self.stdout.write('** tst Exception (%s) **' % ' '.join(options['command']))
            self.stdout.write(format_exc())


def tst_command(self, args):
    if args:
        # log('tst %s' % args)
        cmd = args[0]
        args = args[1:]
        if cmd == 'edit':
            tst_edit(self,args)
        elif cmd == 'find':
            print(tst_find())
        elif cmd == 'list':
            print(tst_list())
        elif cmd == 'output':
            tst_output(self,args)
        elif cmd == 'run':
            tst_run()
            self.stdout.write(tst_results())
        elif cmd == 'like':
            tst_like(self,args)
        elif cmd == 'quick':
            quick_test()
        elif cmd == 'reset':
             Test.objects.all().delete()
        elif cmd == 'results':
            self.stdout.write(tst_results())
        else:
            tst_help(self)
    else:
        tst_run()
        self.stdout.write(tst_results())


def test_dictionary():

    def module_list(directory):
        return [f.replace('.py', '') for f in listdir(directory) if f.endswith('_test.py')]

    def test_name(module):
        return module.replace('_test','').replace('_','-')

    tests = {}
    for m in module_list(TEST_DIR):
        t = test_map(m)
        if t:
            tests[test_name(m)] = t
    return tests


def tst_diff(test_name):
    t = Test.objects.get(name=test_name)
    if not t.expected:
        t.expected = 'Initial expectation'
        t.save()
    if t.output != t.expected:
        diffs = differences(t.output, t.expected)
        return diffs


def tst_edit(self, args):
    system('e %s' % args[0]+'_test.py')


def tst_find():
    tests = test_dictionary()
    functions = []
    for f in sorted(tests):
        functions.append(f)
        for t in tests[f]:
            functions.append('   %s' % t[0])
    return '\n'.join(functions)


def tst_help(self):
    self.stdout.write('''
        script to manage tests

        usage: x tst [command]

        command:
            edit   t    - edit the test file
            find        - find the source code for all tests
            list        - list the test cases
            reset       - update the list of available tests

            run     t   - run a test (or all tests)
            output  t   - show output for a test (or all tests)
            results t   - show test results (or all results)
            like    t   - approve of one or more test results

        ''')


def tst_like(self,args):
    if args:
        t = Test.objects.get(name=args[0])
        t.expected = t.output
        t.save()
        self.stdout.write("Like: "+t.name)
    else:
        tests = Test.objects.all()
        if tests:
            for t in tests:
                if t.output != t.expected:
                    t.expected = t.output
                    t.save()
                    self.stdout.write("Like: "+t.name)
        else:
            self.stdout.write('no tests found')


def tst_list():
    tests = Test.objects.all().order_by('name')
    return '\n'.join([t.name for t in tests])


# TODO: Simplify this
m = ''   # Needed for test_map()


def test_map(module_name):

    def test_entry(entry):
        return (entry[0].replace('_test','').replace('_','-'), entry[1])

    def tests(module):
        functions = getmembers(module, isfunction)
        return [test_entry(f) for f in functions if f[0].endswith('_test')]

    def get_module(module_name):
        global m
        exec('import test.%s; global m; m = test.%s' % (module_name, module_name))
        return m

    return tests(get_module(module_name))


def tst_output(self,args):
    if args:
        t = Test.objects.filter(name=args[0])
        if not t:
            self.stdout.write('Could not find test case: %s' % args[0])
        else:
            self.stdout.write(banner(t[0].name))
            self.stdout.write(t[0].output)

    else:
        tests = Test.objects.all()
        if tests:
            for t in tests:
                self.stdout.write(banner(t.name))
                self.stdout.write(t.output)
        else:
            self.stdout.write('no tests found')


def tst_register(tests):
    for m in tests:
        for t in tests[m]:
            if not Test.objects.filter(name=t[0]):
                Test.objects.create(name=t[0])


def tst_results():

    def show_differences(t):
        if t.expected == None:
             t.expected = 'Initial expectation'
             t.save()
        if t.output != t.expected:
            diffs = differences(t.output, t.expected)
            return banner(t.name)+diffs

    tests = Test.objects.all().order_by('name')
    if tests:
        return '\n'.join([show_differences(t) for t in tests if show_differences(t)])
    else:
        return 'no tests found'


def tst_run():

    def run_test(test_entry):
        text = test_entry[1]()
        if not text:
            text = 'no output'

        test_record = Test.objects.get(name=test_entry[0])
        test_record.output = text
        test_record.save()

    tests = test_dictionary()
    tst_register (tests)
    print("running tests ...")

    for m in sorted(tests):
        print('%s' % m)
        for test_entry in tests[m]:
            run_test(test_entry)

