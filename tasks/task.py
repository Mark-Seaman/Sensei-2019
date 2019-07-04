from datetime import datetime, timedelta
from django.db.models import Sum
from os.path import join
from re import search, findall

from bin.shell import read_file
from bin.switches import TODO_FILES, TODO_DIR
from bin.web import web
from tasks.models import Task
from tasks.summary import work_types
from tool.log import log


# ----------------------------
# Command Interpreter

def task_command(self, args):
    log('task %s' % args)
    if args:
        cmd = args[0]
        args = args[1:]
        if cmd == 'add':
            task_add(self, args)
        elif cmd == 'delete':
            task_delete(self, args)
        elif cmd == 'edit':
            task_edit(self, args)
        elif cmd == 'get':
            task_get(self, args)
        elif cmd == 'health':
            print(task_read_health(args))
        elif cmd == 'import':
            task_import(args)
        elif cmd == 'history':
            task_history(args)
        elif cmd == 'list':
            task_list(self, args)
        elif cmd == 'month':
            task_month(args)
        elif cmd == 'read':
            task_read_events(args)
        elif cmd == 'rename':
            task_rename(args)
        elif cmd == 'summary':
            task_summary(args)
        elif cmd == 'totals':
            task_print_types()
        elif cmd == 'web':
            task_web()
        elif cmd == 'week':
            task_week(args)
        elif cmd == 'work':
            task_work()
        else:
            task_help(self)
    else:
        self.stdout.write('No command given')
        task_help(self)


def task_help(self):
    self.stdout.write('''

        usage: x command 
        
        command:
            add     - add a new record
            delete  - delete a task
            edit    - update a record
            get     - lookup a specific task
            help    - show command help
            import  - import the tasks from a history file
            history - show the task history
            list    - show a list of tasks
            month   - show monthly summary
            read    - read a task history file
            summary - show a summary
            totals  - list all of the task types
            week    - show weekly summary
            work    - show work summary
    ''')


# ----------------------------
# Function

def days_ago(days):
    return datetime.now() - timedelta(days=days)


def hourly_total(tasks):
    return tasks.aggregate(Sum('hours'))['hours__sum']


def monthly_hours_invested(task_type, year, month):
    tasks = tasks_monthly(year, month)
    if task_type:
        tasks = tasks.filter(name=task_type)
    return hourly_total(tasks)


def last_month_hours_invested(task_type):
    tasks = tasks_last_month()
    if task_type:
        tasks = tasks.filter(name=task_type)
    return hourly_total(tasks)


def tasks_last_month():
    end = datetime.now()
    start = end - timedelta(days=60)
    return Task.objects.filter(date__gt=start, date__lte=end)


def task_data_table():
    query = lambda t: last_month_hours_invested(t)
    hours = query(None)
    categories = task_details(query, hours)
    total = [{'name': '   Total', 'hours': "%s" % hours, 'percent': 100}]
    categories = sort_totals(total + categories)
    return [x for x in categories if x and x['hours']]


def monthly_totals(year, month):
    query = lambda t: monthly_hours_invested(t, year, month)
    hours = query(None)
    categories = task_details(query, hours)
    total = [{'name': '   Total', 'hours': "%s" % hours, 'percent': 100}]
    categories = sort_totals(total+categories)
    return [x for x in categories if x and x['hours']]


def full_totals():
    query = lambda t: total_hours_invested(t)
    hours = query(None)
    categories = task_details(query, hours)
    total = [{'name': '   Total', 'hours': "<b>%s</b>" % hours}]
    categories = sort_totals(total+categories)
    return [x for x in categories if x and x['hours']]


def print_summary(summary, start=None, end=None):
    if start and end:
        print("From %s through %s" %  (start.strftime('%a, %Y-%m-%d'), end.strftime('%a, %Y-%m-%d')))
    for x in summary:
        print('%-12s %4s' % (x['name'], x['hours']))


def recent_weeks():
    return [days_ago(days*7).strftime('%Y-%m-%d') for days in range(12)]


def recent_months():
    return ['2016-%02d'%(m+1) for m in range(12)] + ['2017-%02d'%(m+1) for m in range(5)]


def sort_totals(categories):
    return sorted(categories, key=lambda x: x['hours'], reverse=True)


def task_add(self, args):
    if not args:
        self.stdout.write('A task must have a name')
    else:
        task = Task.objects.create()
        task_set_name(args, task)


def task_delete(self, args):
    if not args:
        # Task.objects.all().delete()
        self.stdout.write('You must specify a task')
        return

    tasks = Task.objects.filter(pk=args[0])
    if args and tasks:
        tasks[0].delete()
    else:
        self.stdout.write('Could not find task, %s' % args[0])


def task_details(query, hours):

    def record(name, hours, total):
        if hours:
            return {
                'name': name,
                'hours': hours,
                'percent': (hours*100/total),
            }

    return [record(t, query(t), hours) for t in task_types() if query(t)]


def task_doc_path(args):
    if args:
        if type(args) == type([]):
            return join(TODO_DIR, args[0])
        else:
            return join(TODO_DIR, args)
    else:
        return TODO_FILES[1]


def task_edit(self, args):
    tasks = Task.objects.filter(pk=args[0])
    if tasks:
        task_set_name(args[1:], tasks[0])
    else:
        self.stdout.write('Could not find task, %s' % args[0])


def task_get(self, args):
    tasks = Task.objects.filter(pk=args[0])
    if tasks:
        t = tasks[0]
        self.stdout.write("ID:    %s" % t.pk)
        self.stdout.write("Name:  %s" % t.name)
        self.stdout.write("Date:  %s" % t.date)
    else:
        self.stdout.write('Could not find task, %s' % args[0])


def task_import(args):
    if args:
        tasks = task_read_events(args)
        year = args[0][:4]
    else:
        tasks = task_read_events(TODO_FILES[0])
        year = '2018'
    for t in tasks:
        x = t[0][5:].split('-')
        date = '%s-%s-%s' % (year, x[0], x[1])
        name = t[1]
        hours = t[2]
        notes  = t[3]
        e = Task.objects.get_or_create(date=date, name=name)[0]
        e.hours = hours
        e.notes = notes
        e.save()
        print('%s  %s  %s  \n%s\n' % (e.date, e.name, e.hours, e.notes))


def task_history(args):

    def print_task_history(tasks):
        for t in tasks:
            print('%s\n' % t.date)
            print('    %s %s' % (t.name, t.hours))
            if t.notes:
                print(t.notes + '\n')

    if args:
        task = args[0]
        print('# %s Task History\n\n' % task)

    else:
        task = None
        print('# History for All Tasks\n\n' )
    tasks = task_select(task, None, None)
    print_task_history(tasks)
    return tasks


def task_list(self, args):
    self.stdout.write('  '.join(["%-10s" % x for x in Task.labels()]))
    for t in Task.objects.all():
        self.stdout.write('  '.join(["%-10s" % x for x in t.as_row()]))


def task_month(args):
    if args:
        year, month = args[0].split('-')
        summary = monthly_totals(year, month)
        print_summary(summary)
    else:
        print('usage: task month 2017-01')


# def task_read_events(args):
#     lines = read_file(task_doc_path(args)).split('\n')
#     events = list_events(args)
#     return [e for e in append_tasks(events, lines) if len(e) > 2]


def task_read_health(args):
    # print('TASKS (%s)' % read_file(task_doc_path(args)))
    events = []
    text = read_file(task_doc_path(args))
    date_pattern = r'^([A-Za-z]+, \d\d-\d\d) *$'
    health_pattern = r'^    +(\d, *\d, *\d, *\d)'
    day = ''
    for line in text.split('\n'):
        x = search(date_pattern, line)
        if x:
            day = line.strip()
        health = findall(health_pattern, line)
        if health:
            # print('%s, %s' % (day, health[0]))
            events.append('%s, %s' % (day, health[0]))
    return events


def task_rename(args):
    for t in Task.objects.filter(name=args[0]):
        print('%12s %12s' % (t.date, t.name))
        t.name = args[1]
        t.save()


def task_set_name(args, task):
    task.name = ' '.join(args)
    task.save()


def task_select(task_type=None, date=None, days=None):
    if days:
        end = datetime.now()
        start = end - timedelta(days)
        tasks = Task.objects.filter(date__gt=start, date__lte=end)
    else:
        tasks = Task.objects.all()
    if task_type:
        tasks = tasks.filter(name=task_type)
    return tasks


def task_summary(args):
    print('task summary')
    text = read_file(TODO_FILES[1])
    x = findall(r'\n(\w{3}, \d\d-\d\d *- \d *)\n', text)
    for m in x:
        print(m)


def task_totals():
    query = lambda t: total_hours_invested(t)
    categories = task_details(query, 1)
    total = [{'name': '   Total', 'hours': query(None)}]
    return [x for x in categories + total if x['hours']]


def task_types():
    types = Task.objects.order_by('name').distinct()
    return (set([t.name for t in types]))


def task_print_types():
    summary = task_totals()
    print_summary(summary)


def task_web():
    web('http://shrinking-world.com/task')


def task_week(args):
    if args:
        year, month, day = args[0].split('-')
    else:
        yesterday = datetime.now()-timedelta(days=1)
        year, month, day = yesterday.strftime('%Y-%m-%d').split('-')
    summary = weekly_totals(year, month, day)
    print_summary(summary, datetime.now()-timedelta(days=7), datetime.now()-timedelta(days=1))


def task_work():
    summary = task_totals()
    total = 0
    x = ''
    for x in summary:
        if x['name'] in work_types():
            print('%-12s %4s' % (x['name'], x['hours']))
            total += int(x['hours'])
    hours = int(x['hours'])
    print("\n    Work     %s hours" % total)
    print("    Total    %s hours" % x['hours'])
    print("    Work      %s%%" % (total * 100 / hours))


def tasks_monthly(year, month):
    return Task.objects.filter(date__year=year, date__month=month)


def tasks_weekly(year, month, day):
    end = datetime(year=int(year), month=int(month), day=int(day))
    start = end - timedelta(days=7)
    return Task.objects.filter(date__gt=start, date__lte=end)


def total_hours_invested(task_type):
    tasks = Task.objects
    if task_type:
        tasks = tasks.filter(name=task_type)
    # log('total hours', len(tasks))
    return hourly_total(tasks)


def weekly_hours_invested(task_type, year, month, day):
    tasks = tasks_weekly(year, month, day)
    if task_type:
        tasks = tasks.filter(name=task_type)
    return hourly_total(tasks)


def weekly_totals(year, month, day):
    query = lambda t: weekly_hours_invested(t, year, month, day)
    categories = task_details(query, query(None))
    total = [{'name': '   Total', 'hours': query(None)}]
    return [x for x in categories + total if x['hours']]


def task_report(year, month):

    def query_month_tasks(year, month):
        tasks = Task.objects.filter(date__month=month, date__year=year).order_by('date')
        dates = tasks.values('date').distinct()
        dates = [t['date'] for t in dates]
        return [(t.strftime("%a, %m-%d"), Task.objects.filter(date=t)) for t in dates]

    def task_entry(task):
        notes = task.notes if task.notes else ''
        notes = [n for n in notes.split('\n') if n]
        notes = '\n'.join(notes)
        # notes = notes.decode(encoding='UTF-8').encode('ascii', 'ignore')
        return '%s %s\n\n%s\n' % (task.name, task.hours, notes.encode('ascii', 'ignore'))

    report = []
    for day in query_month_tasks(year, month):
        tasks = '\n    '.join([task_entry(t) for t in day[1]])
        report.append('\n\n%s\n\n    %s\n'%(day[0], tasks))
    return ''.join(report)


def save_monthly_reports(year):

    def save_report(report, month):
        path = join('Documents', 'info', 'history', 'months', month)
        with open(path, 'w') as f:
            f.write('# Tasks History     %s\n\n## Accomplishments\n\n' % month)
            f.write(report)

    reports = []
    for m in range(12):
        month = "%02d" % (m+1)
        file = "%s-%02d" % (year, m+1)
        save_report(task_report(year, month), file)
        reports.append(month)
    return reports


