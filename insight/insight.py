from insight.models import Insight
from django.utils.timezone import make_aware
from csv import reader
from datetime import datetime


def date_str(date):
    return date.strftime("%a %Y-%m-%d")


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
        insights.append([topic, [(date_str(i.date), i.name) for i in Insight.objects.filter(topic=topic)]])
    return insights


def print_insights():
    for topic in group_insights():
        print("\n%s" % topic[0])
        for i in topic[1]:
            print("    %s - %s" % (i[0], i[1]))


def sync_insights():
    import_data('insights.csv')
    export_data('insights.csv')


def topics():
    return [i[0] for i in Insight.objects.all().order_by('topic').values_list('topic').distinct()]

