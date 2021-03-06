from django.core.management.base import BaseCommand
from os import system
import traceback

from tool.log import log_exception

host = 'seamanfamily.org'


# ----------------------------------
# Command Interpreter


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('script', nargs='+', type=str)

    def handle(self, *args, **options):
        try:
            ocean_command(self, options['script'])
        except:
            log_exception()
            self.stdout.write('** tst Exception (%s) **' % ' '.join(options['script']))
            self.stdout.write(traceback.format_exc())


def ocean_command(self, options):
    '''Execute all of the brain specific brains'''
    # self.stdout.write('starting ocean command ...')

    if options:
        cmd = options[0]
        args = options[1:]

        if cmd == 'console':
            console(args)
        elif cmd == 'deploy':
            system('./manage.py vc commit deploy %s' % ' '.join(args))
            deploy(args)
        elif cmd == 'log':
            log(args)
        elif cmd == 'restart':
            restart()
        elif cmd == 'root':
            root()
        elif cmd == 'serve':
            runserver()
        elif cmd == 'web':
            web()
        else:
            print('No ocean command found, ' + cmd)
            ocean_help()
    else:
        print('No arguments given')
        ocean_help()
    # self.stdout.write('... ending  ocean command')


def ocean_help():
    print('''
    usage:  brain cmd [args]

    cmd:

        console - Open a terminal on the Digital Ocean droplet

        deploy - Send code to server 

        log - Show the system log

        restart - Restart the remote web server

        root - Login to remote server as root
        
        serve - Run the local web server

        web - Browse to the Brain App web page

    ''')


def console(args):
    commmand = ' '.join(args)
    print('Remote Command: %s' % commmand)
    system('ssh sensei@%s %s' % (host,commmand))


def deploy(args):
    # system('bluepush')
    console(['bin/commit SENSEI_AUTO_COMMIT'])
    restart()
    web()
    console(['". bin/bashrc && python manage.py tst"'])


def log(args):
    console(['". bin/bashrc && python manage.py log"'])


def restart():
    print('Sensei Server Restart:  systemctl restart gunicorn')
    system('ssh root@%s %s' % (host, 'systemctl restart gunicorn'))


def root():
    system('ssh root@%s' % host)


def runserver():
    system('cd ~/Brain && ./manage.py runserver 8004')


def web():
    url = 'http://'+host
    system('open -a "Firefox" %s' % url)
