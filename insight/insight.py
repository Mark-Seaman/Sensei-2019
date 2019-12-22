from calendar import monthrange, month_name
from csv import reader
from datetime import datetime
from django.template.loader import render_to_string
from django.utils.timezone import make_aware

from insight.models import Insight
from tool.days import date_str


def export_data(path):
    with open(path, 'w') as f:
        for row in Insight.objects.filter(date__gte='2019-12-01').order_by('date'):
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


def find_topics(topic):
    return Insight.objects.filter(topic=topic).order_by('date')


def find_monthly_insights(year, month):
    return Insight.objects.filter(date__year=year, date__month=month).order_by('date')


def topic_insights_panel(title, topic):
    headers = ['Date', 'Insight']
    return [topic, render_panel(title, headers, find_topics(topic))]


def topic_insights():
    insights = []
    for topic in topics():
        title = "Insight Category: %s" % topic
        insights.append(topic_insights_panel(title, topic))
    return dict(groups=insights[1:])


def monthly_insights_panel(year, month, active):
    title = 'Monthly Insights: %s %s' % (month_name[month], year)
    headers = ['Date', 'Topic', 'Creative Experience']
    rows = find_monthly_insights(year, month)
    table = render_panel(title, headers, rows)
    return [month_name[month], table, active, not active]


def monthly_insights():
    monthly = [
        monthly_insights_panel(2019, 9,  False),
        monthly_insights_panel(2019, 10, False),
        monthly_insights_panel(2019, 11, False),
        monthly_insights_panel(2019, 12, True),
    ]
    return dict(groups=monthly)


# def print_insights():
#     for topic in topic_insights():
#         print("\n%s" % topic[0])
#         for i in topic[1]:
#             print("    %s - %s" % (i[0], i[1]))


def render_panel(title, headers, rows):
    return render_to_string('table.html', dict(title=title, headers=headers, rows=rows))


def sync_insights():
    import_data('insights.csv')
    export_data('insights.csv')


def task_history(insight):
    return 'Documents/info/history/%s' % date_str(insight.date).replace('-', '/')


def topics():
    return [i[0] for i in Insight.objects.all().order_by('topic').values_list('topic').distinct()]


