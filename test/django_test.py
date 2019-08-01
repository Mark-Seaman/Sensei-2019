from tool.shell import hostname, is_server, shell, shell_script


def django_hammer_test():
    return shell('ls -l hammer|grep -v sensei.db')


def django_settings_test():
    return shell('cat hammer/settings.py')


def django_webserver_test():
    if is_server():
        return shell('cat hammer/wsgi.py /etc/systemd/system/gunicorn.service /etc/nginx/sites-available/sensei')
    else:
        config = shell('cat hammer/wsgi.py hammer/config/gunicorn.conf hammer/config/nginx.conf')
        return '%s is not the Server. Configuration is not active. \n\n%s' % (hostname(), config)


def django_python_version_test():
    return shell('python --version')


def django_python_path_test():
    return shell('which python')


def django_pipenv_test():
    return shell('pip list')


def django_shell_script_test():
    command_string = 'cat tool/shell.py|grep def'
    return shell_script(command_string)

