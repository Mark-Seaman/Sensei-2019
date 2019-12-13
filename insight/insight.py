from csv import reader
from datetime import datetime
from django.template.loader import render_to_string
from django.utils.timezone import make_aware

from insight.models import Insight
from tool.days import date_str


def export_data(path):
    with open(path, 'w') as f:
        for row in Insight.objects.all():
            f.write("%s,%s,%s\n" % (row.date.strftime("%Y-%m-%d"), row.topic, row.name))


def import_data(path):
    # Insight.objects.all().delete()
    with open(path) as f:
        for row in reader(f):
            date = make_aware(datetime.strptime(row[0], "%Y-%m-%d"))
            i = Insight.objects.get_or_create(date=date)[0]
            i.topic = row[1]
            i.name = row[2]
            i.save()


def group_insights():
    insights = []
    for topic in topics():
        title = "Insight Category: %s" % topic
        table = [(date_str(i.date), i.name) for i in Insight.objects.filter(topic=topic)]
        insights.append([topic, render_panel(title, ['Date', 'Insight'], table)])
    return insights[1:]


def render_panel(title, headers, rows):
    return render_to_string('table.html', dict(title=title, headers=headers, rows=rows))


def daily_insights(month, days):
    title = "Monthly Insights: %s" % month
    headers = ['Date', 'Topic', 'Creative Experience']
    rows = [(d, Insight.lookup(d).name, Insight.lookup(d).pk, Insight.lookup(d).topic) for d in days]
    table = render_panel(title, headers, rows)
    return [month, table]


def monthly_insights(months):
    days1 = ['2019-10-%02d' % (d + 1) for d in range(31)]
    days2 = ['2019-11-%02d' % (d + 1) for d in range(30)]
    monthly = [daily_insights('October', days1), daily_insights('November', days2)]
    return dict(months=monthly)


def print_insights():
    for topic in group_insights():
        print("\n%s" % topic[0])
        for i in topic[1]:
            print("    %s - %s" % (i[0], i[1]))


def sync_insights():
    import_data('insights.csv')
    export_data('insights.csv')


def task_history(insight):
    return 'Documents/info/history/%s' % date_str(insight.date).replace('-', '/')


def topics():
    return [i[0] for i in Insight.objects.all().order_by('topic').values_list('topic').distinct()]


def render_insights(insights):
    return render_to_string('insight_groups.html', dict(insights=insights))