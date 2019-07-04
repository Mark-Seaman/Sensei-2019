
def fix_tasks_notes():
    from tasks.models import Task
    tasks = Task.objects.all()
    for t in tasks:
        if t.notes:
            x = t.notes.encode('utf-8', 'ignore')
            t.notes = x
            t.save()


def fix_tasks_name():
    from tasks.models import Task
    for t in Task.objects.filter(name='Teach'):
        t.name = 'UNC'
        t.save()
    print(len(Task.objects.filter(name='Teach')))


def cleanup_records():
    from tasks.models import Task
    for t in Task.objects.filter(hours='0'):
        if t.notes.strip() == '':
            t.delete()


cleanup_records()

def test_tasks():
    from tasks.models import Task
    tasks = Task.objects.all()
    for t in tasks:
        if t.notes:
            x = t.notes.encode('utf-8', 'ignore')
            t.notes = x
            t.save()

from tasks.models import *

def list_tasks(date):
    for t in Task.objects.filter(date=date):
        print ('%s %s' % (t.name, t.hours))
