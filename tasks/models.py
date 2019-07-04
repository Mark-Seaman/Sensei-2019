from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


# Task
class Task (models.Model):
    name     = models.CharField (max_length=100)
    notes    = models.TextField (null=True, blank=True)
    date     = models.DateField (default=now)
    hours    = models.IntegerField (default=0)
    done     = models.BooleanField (default=False)
    # project  = models.ForeignKey (Project, on_delete=models.CASCADE)
    # client   = models.ForeignKey (User, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.name + ', ' + str(self.date)

    # def get_absolute_url(self):
    #     return reverse('church-score-detail', kwargs={'pk': self.pk})

    def as_row(self):
        return [self.pk, self.name, self.date, self.hours, self.notes.split('\n') if self.notes else None]

    @staticmethod
    def labels():
        return ['ID', 'Activity', 'Date', 'Hours', 'Details']


#
# GoalClient
# * name
# * user (User)
#
# ProjectType
# * name
# * client (GoalClient)
#
# Project
# * name
# * type (ProjectType)
# * notes
# * investment_estimate
# * benefits
# * priority
#
# TaskType
# * name
# * client (GoalClient)
#
# Task
# * date
# * hours
# * task
# * type (TaskType)
# * project (Project)
#
# WeeklyReview
# * date
# * notes
# * client (GoalClient)
#
# MonthlyReview
# * date
# * notes
# * client (GoalClient)
#
# LifeGoal
# * client (GoalClient)
# * name
# * notes
