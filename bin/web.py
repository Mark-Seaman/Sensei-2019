#!/usr/bin/env python

from os import environ, system
from os.path import  abspath, exists, join
from platform import node
from sys import argv


def web_command(args):
    '''Execute all of the web specific webs'''
    if args:
        web(args[0])
    else:
        web('https://markseaman.info')


def web_help():
    '''Show all the web webs and their usage.'''
    print('''
    usage:  web page
            ''')


def web(page):
    '''Open a web page in Google Chrome'''
    url = page
    if not page.startswith('http://') and not page.startswith('https://'):
        if exists(page):
            url = 'file://' + abspath(page)
        else:
            url = 'http://' + page
    print('firefox %s' % url)
    # Use the correct invocation
    if 'iMac' in node() or 'mac' in node():
        # system('open -a "Google Chrome" '+url)
        system('open -a "Firefox" '+url)
    else:
        system('start chrome '+url)


def web_path(topic=None):
    path = environ['pb']
    if topic:
        path = join(path,topic)
    return path



'''
Create a script that can be run from the shell
'''
if __name__=='__main__':
    web_command(argv[1:])

