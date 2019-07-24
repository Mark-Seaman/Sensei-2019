from tool.shell import shell
from tool.management.commands.tst import tst_find, tst_list


def tst_code_test():
    return open('tool/management/commands/tst.py').read()


def tst_list_test():
    return tst_list()


def tst_find_test():
    return tst_find()


def tst_files_test():
    return shell('ls -l test')


def tst_run_time_test():
    return shell('date')
