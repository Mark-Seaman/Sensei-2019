from datetime import datetime, timedelta
from django.db.models import Sum

from tasks.models import Task


def tasks_monthly(year, month):
    return Task.objects.filter(date__year=year, date__month=month)


def recent_months():
    return ['2016-%02d'%(m+1) for m in range(12)] + ['2017-%02d'%(m+1) for m in range(7)]


def months_data_table():
    table = []
    for m in recent_months():
        year,month = m.split('-')
        task_hours = tasks_monthly(year, month).aggregate(total=Sum('hours'))
        if task_hours['total']:
            table.append([m, task_hours['total']])
    labels = ['Task Name', 'Invested Time', 'Percentage']
    return {
        'labels': labels,
        'table': table,
    }


def tasks_data_table(days):
    end = datetime.now()
    start = end - timedelta(days=days)
    tasks = Task.objects.filter(date__gt=start, date__lte=end)
    totals = tasks.values('name').annotate(task_hours=Sum('hours')).order_by('-task_hours')
    total = sum([t['task_hours'] for t in totals])
    table = [(t['name'], t['task_hours'], t['task_hours'] * 100 / total) for t in totals]
    labels = ['Task Name', 'Invested Time', 'Percentage']

    return {
        'total': total,
        'labels': labels,
        'table': table,
    }


def days_data_table(days):
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


# from tasks.models import Task
#
# def task_list(task):
#     for t in Task.objects.filter(name=task):
#         print(t.date, t.name, t.hours, t.notes)
#         t.name = 'Business'
#         t.save()
#
# task_list('Work')
# task_list('Family')

# def task_list(date):
#     for t in Task.objects.filter(date=date):
#         print(t.date, t.name, t.hours)
        # if t.name == 'Fun':
        #     t.hours = 3
        #     t.save()
        # if t.name == 'Grow':
        #     t.hours = 1
        #     t.save()
        #      t.delete()


# task_list('2017-01-01')

