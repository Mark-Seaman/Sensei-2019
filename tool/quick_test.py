from django.contrib.auth.models import User

from tool.user import list_users
from unc.bacs import *
from unc.models import *


def quick_test():
    import_test_students()
    add_teacher()


def add_teacher():
    course_name = 'bacs200'
    name = 'MarkSeaman'
    email = 'mark.b.seaman@gmail.com'
    domain = r'https://unco-bacs.org'
    c = Course.lookup(course_name)
    u = User.objects.get(username=name)
    s = Student.objects.get_or_create(name=name, email=email, course=c, user=u)[0]
    s.user = u
    s.domain = domain
    s.save()

    print(list_users())
    print(print_students(course_name))