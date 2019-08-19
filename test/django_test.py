from pprint import PrettyPrinter
from tool.text import text_join

from tool.document import resize_image
from tool.shell import hostname, is_server, shell, shell_script


def format_dictionary(features):
    return PrettyPrinter(indent=4, width=200).pformat(features)


def django_hammer_test():
    return shell('ls -l hammer|grep -v sensei.db')


def django_image_resize_test():
    infile = '/Users/seaman/UNC/MarkSeaman/Mark-Seaman-800.jpg'
    outfile = infile.replace('800', '100')
    size = 100
    return resize_image(infile, outfile, size)


def django_dictionary_test():
    d = [
        {'student': 'Mark Seaman', 'url': 'http://unco-bacs.org/bacs200/index.html', 'requirements': 42 },
        {'student': 'sad Seaman', 'url': 'http://unco-bacs.org/bacs200/index.html', 'requirements': 42},
        {'student': 'dsaf Seaman', 'url': 'http://unco-bacs.org/bacs200/index.html', 'requirements': 42},
        {'student': 'sdaf Seaman', 'url': 'http://unco-bacs.org/bacs200/index.html', 'requirements': 42},
    ]
    return format_dictionary(d)


def django_python_version_test():
    return shell('python --version')


def django_python_path_test():
    return shell('which python')


def django_pipenv_test():
    return shell('pip list')


def django_settings_test():
    return shell('cat hammer/settings.py')


def django_shell_script_test():
    command_string = 'cat tool/shell.py|grep def'
    return shell_script(command_string)


def django_webserver_test():
    if is_server():
        return shell('cat hammer/wsgi.py /etc/systemd/system/gunicorn.service /etc/nginx/sites-available/sensei')
    else:
        config = shell('cat hammer/wsgi.py hammer/config/gunicorn.conf hammer/config/nginx.conf')
        return '%s is not the Server. Configuration is not active. \n\n%s' % (hostname(), config)


