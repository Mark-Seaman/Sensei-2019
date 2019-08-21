from tool.user import list_users
from unc.bacs import import_test_students, print_students


def quick_test():
    import_test_students()
    print(list_users())
    print(print_students('bacs200'))

