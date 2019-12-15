from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import make_aware
from django.urls import reverse
from tool.days import to_date


def date_str(date):
    return date.strftime("%a %Y-%m-%d")


class Insight(models.Model):
    name = models.CharField(max_length=100)
    topic = models.CharField(max_length=20)
    date = models.DateField(null=True)

    def get_absolute_url(self):
        return reverse('insight-list')

    def __str__(self):
        return '%s - %s - %s' % (date_str(self.date), self.topic, self.name)

    @staticmethod
    def lookup(date):
        date = make_aware(to_date(date))
        return Insight.objects.get_or_create(date=date)[0]




