from tool.shell import hostname, is_server, shell
from tool.files import recursive_list


def system_files_test():
    return shell('ls -l') + shell('pwd')


def system_python_files_test():
    files = [f for f in recursive_list('.') if f.endswith('.py') and not f.startswith('sensei/env/') and not f.startswith('.venv/')]
    return '\n'.join(files)


def system_server_test():
    return 'Hostname: %s, IsServer: %s' % (hostname(), is_server())