from django.db.models import Sum
from datetime import datetime, timedelta
from os import listdir, mkdir
from os.path import exists, join

from tasks.models import Task


def activity_summary(activity):
    def active_tab(a, t):
        return 'active' if t == a else ''

    if activity == 'Work':
        activities = work_types()
        activity = 'UNC'
    else:
        activities = [activity]

    summary = [(t, task_activity_details(t), active_tab(activity, t)) for t in activities]
    summary = sort_activity(summary)
    return summary


def activities_work():
    return ['WAM', 'Sign', 'UNC', 'Business', 'Tools', 'Hammer', 'Hire', 'Write', 'Aspire']


def sort_activity(data):
    data = [t for t in data if len(t[1]) > 0]
    return sorted(data, key=lambda x: len(x[1]), reverse=True)


def bad_days():
    end = datetime.now()
    start = end - timedelta(days=365)
    tasks = Task.objects.filter(date__gt=start, date__lte=end)
    totals = tasks.values('date').annotate(task_hours=Sum('hours')).order_by('-date')
    return [(t['date'], t['task_hours']) for t in totals if t['task_hours'] != 14]


def bad_days_data(days):
    end = datetime.now()
    start = end - timedelta(days=days)
    tasks = Task.objects.filter(date__gt=start, date__lte=end)
    totals = tasks.values('date').annotate(task_hours=Sum('hours')).order_by('-date')
    total = sum([t['task_hours'] for t in totals])
    table = [(t['date'], t['task_hours']) for t in totals if t['task_hours'] != 14]
    labels = ['Date', 'Invested Time']

    return {
        'total': total,
        'labels': labels,
        'table': table,
    }


def combine_work_tasks(table, total):
    work = 0
    results = []
    for row in table:
        if row[0] in activities_work():
            work += row[1]
        else:
            results.append(row)
    if total != 0:
        results = [('Work', work, work * 100 / total)] + results
        return results


def tasks_activity(activity):
    print('activity', activity)
    tasks = Task.objects.filter(name=activity)
    tasks = time_filter(tasks, 31)
    return tasks.order_by('-date')


def task_activity_details(activity):
    return [task_detail(task) for task in tasks_activity(activity)]


def task_detail(task):
    details = task.notes.split('\n') if task.notes else []
    details = [t for t in details if t.strip()]
    return [task.pk, task.name, task.date, task.hours, details]


def query_hours(task, days):
    tasks = Task.objects.all()
    tasks = task_filter(tasks, task)
    tasks = time_filter(tasks, days + 1)
    totals = tasks.values('name').annotate(task_hours=Sum('hours')).order_by('-task_hours')
    total = sum([t['task_hours'] for t in totals])
    return '%s' % total


def task_filter(tasks, activity):
    if activity == 'Work':
        return tasks.filter(name__in=work_types())
    return tasks.filter(name=activity)


def time_data():
    times = [''] + ['Week', 'Month', 'Year']
    tasks = ['Work', 'People', 'Church', 'Grow', 'Fun']
    days = [7, 30, 365]
    totals = [[t] + [query_hours(t, d) for d in days] for t in tasks]
    subtotals = time_totals(totals)
    return dict(times=times, tasks=tasks, hours=totals,
                time_totals=time_totals(totals),
                task_totals=percent_totals(totals, subtotals),
                review=review_totals(totals, subtotals))


def time_totals(totals):
    def time_total(totals, time):
        x = 0
        for t in totals:
            x += int(t[time])
        return x

    return [time_total(totals, time) for time in [1, 2, 3]]


def percent(actual, total):
    if total == 0:
        return 0
    else:
        return int((int(actual) * 100 + 5) / total)


def percent_totals(totals, subtotals):
    return [[task[0]] + [percent(hours, subtotals[i]) for i, hours in enumerate(task[1:])] for task in totals]


def review_totals(totals, subtotals):
    def percent_difference(actual, total, ideal):
        diff = percent(actual, total) - ideal
        if diff < -1 or diff > 1:
            return "%s%%" % diff
        else:
            return ''

    def task_percents(totals, task, index, ideals):
        return [percent_difference(hours, totals[i], ideals[index]) for i, hours in enumerate(task[1:])]

    ideals = [40, 20, 10, 10, 20]
    return [[task[0]] + task_percents(subtotals, task, index, ideals) for index, task in enumerate(totals)]


def time_filter(tasks, days):
    end = datetime.now()
    start = end - timedelta(days=days)
    print('time filter', start, end)
    return tasks.filter(date__gt=start, date__lte=end)


def task_text_list(tasks):

    def format(t):
        return "%s %s\n\n%s\n" % (t.name, t.hours, t.notes.strip('\n').replace('      ', '  '))

    return '\n'.join([format(t) for t in tasks])


def task_list(days=8):

    def daily_report(t):
        date = t.strftime("%Y-%m-%d")
        summary = task_text_list(Task.objects.filter(date=t))
        return date, summary

    tasks = Task.objects.all()
    if days != 'all':
        tasks = time_filter(Task.objects.all(), days)

    dates = tasks.order_by('date').values('date').distinct()
    dates = [t['date'] for t in dates]
    return [daily_report(t) for t in dates]


def time_summary(days):
    tasks = time_filter(Task.objects.all(), days)
    totals = tasks.values('name').annotate(task_hours=Sum('hours')).order_by('-task_hours')
    total = sum([t['task_hours'] for t in totals])
    labels = ['Task Name', 'Invested Time', 'Percentage']
    table = [(t['name'], t['task_hours'], percent(t['task_hours'], total)) for t in totals]
    table = combine_work_tasks(table, total)
    return {
        'total': total,
        'labels': labels,
        'table': table,
    }


def work_types():
    return 'Hire,Aspire,Business,Family,UNC,Tools,WAM,Sign,Write,Hammer'.split(',')


def task_export():

    def export_file(date, tasks):
        year, month, day = date.split('-')
        path = join('Documents', 'info', 'history', year)
        if not exists(path):
            mkdir(path)
        path = join(path, month)
        if not exists(path):
            mkdir(path)
        path = join(path, day)
        open(path, 'w').write(tasks + '\n')

    tlist = task_list('all')
    for t in tlist:
        export_file(t[0], t[1])
    return tlist


def task_import_files():
    def task_details(f):
        return [f, read_task_file(f)]

    def read_task_file(f):
        text = open('Documents/info/days/' + f).read()
        notes = []
        tasks = []
        activity = ''
        hours = ''
        for line in text.split('\n'):
            if line and not line.startswith(' '):
                if notes:
                    t = new_task(f, activity, hours, notes)
                    tasks.append('%s -- %s hours' % (t.name, t.hours))
                words = line.split(' ')
                activity = words[0]
                if words[1:]:
                    hours = words[1]
                else:
                    hours = 0
                notes = []
            elif line:
                notes.append(line)
        if notes:
            t = new_task(f, activity, hours, notes)
            tasks.append('%s -- %s hours' % (t.name, t.hours))
        return '\n\n'.join(tasks)

    def new_task(date, name, hours, notes):
        t = Task.objects.get_or_create(date=date, name=name)[0]
        t.hours = hours
        t.notes = '\n'.join(notes)
        t.save()
        return t

    return [task_details(f) for f in listdir('Documents/info/days')]
