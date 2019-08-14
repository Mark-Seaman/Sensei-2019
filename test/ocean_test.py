from tool.shell import is_server, shell


def ocean_connect_test():
    if is_server():
        return 'Test Disabled on Sensei Server'
    return shell('python manage.py ocean console git status')
