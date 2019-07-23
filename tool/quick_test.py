from tool.management.commands.code import execute_command


def quick_test():
    execute_command('search doc info August')
    execute_command('search html h1 title')
    execute_command('search code info def')


