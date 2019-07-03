from tool.shell import shell


def django_hammer_test():
    return shell('ls -l hammer')


def django_settings_test():
    return shell('cat hammer/settings.py')


def django_webserver_test():
    return shell('cat hammer/wsgi.py /etc/systemd/system/gunicorn.service /etc/nginx/sites-available/sensei')


def django_python_version_test():
    return shell('python --version')


def django_python_path_test():
    return shell('which python')


def django_pipenv_test():
    return shell('pip list')

