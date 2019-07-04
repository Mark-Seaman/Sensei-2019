from tasks.models import Task


def task_records_test():
    return '%s Task Records' % str(len(Task.objects.all()))

