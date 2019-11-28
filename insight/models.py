from csv import reader
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import make_aware
from django.urls import reverse


def date_str(date):
    return date.strftime("%a %Y-%m-%d")


class Insight(models.Model):
    name = models.CharField(max_length=100)
    topic = models.CharField(max_length=20)
    date = models.DateTimeField(null=True)

    def get_absolute_url(self):
        return reverse('insight-list')

    def __str__(self):
        return '%s - %s - %s' % (date_str(self.date), self.topic, self.name)

    @staticmethod
    def lookup(date):
        return Insight.objects.get_or_create(date=date)[0]

    @staticmethod
    def list():
        insights = {}
        for topic in Insight.topics():
            insights[topic] = [(date_str(i.date), i.name) for i in Insight.objects.filter(topic=topic)]
        return insights

    @staticmethod
    def import_data(path):
        # Insight.objects.all().delete()
        with open(path) as f:
            for row in reader(f):
                date = make_aware(datetime.strptime(row[0], "%Y-%m-%d"))
                i = Insight.objects.get_or_create(date=date)[0]
                i.topic = row[1]
                i.name = row[2]
                i.save()

    @staticmethod
    def export_data(path):
        with open(path, 'w') as f:
            for row in Insight.objects.all():
                f.write("%s,%s,%s\n" % (row.date.strftime("%Y-%m-%d"), row.topic, row.name))

    @staticmethod
    def topics():
        return [i[0] for i in Insight.objects.all().order_by('topic').values_list('topic').distinct()]

    @staticmethod
    def print_insights():
        insights = Insight.list()
        for i in insights:
            print("\n%s" % i)
            for x in insights[i]:
                print("    %s - %s" % (x[0], x[1]))

