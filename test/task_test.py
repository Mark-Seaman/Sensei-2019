from tasks.models import Task
from tool.text import text_join
from tool.days import enumerate_days, my_age_in_days, to_date, today


def task_days_age_test():
    return my_age_in_days()


def task_recent_days_test():
    return text_join([d for d in enumerate_days(to_date(today()), 7)])


def task_records_test():
    return '%s Task Records' % str(len(Task.objects.all()))


