from unc.models import *
from unc.bacs import *


def quick_test():
    # Course.objects.filter(pk=1).delete()
    # c = Course.objects.get(name='bacs350')
    # c.teacher = 'Mark Seaman'
    # c.save()
    initialize_data()
    print(print_data())


