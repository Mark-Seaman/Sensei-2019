from tool.shell import shell
from tool.files import recursive_list


def system_files_test():
    return shell('ls -l') + shell('pwd')


def system_python_files_test():
    files = [f for f in recursive_list('.') if f.endswith('.py') and not f.startswith('sensei/env/')]
    return '\n'.join(files)
