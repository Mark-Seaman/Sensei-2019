from calendar import day_abbr, monthrange, month_name, weekday
from datetime import datetime, timedelta


# ------------------------------
# Command Interpreter
from django.utils.timezone import make_aware


def days_command(options):
    if options:
        cmd = options[0]
        args = options[1:]
        if cmd=='list':
            days_list(args)
        elif cmd=='month':
            days_month(args)
        elif cmd=='today':
            print(today())
        elif cmd == 'weeks':
            days_weeks(args[0])
        else:
            days_help(args)
    else:
        days_help()


def days_help(args=None):
    print('''
        days Command

        usage: x days COMMAND

        COMMAND:

            list    - list the document files
            month   - list the days in a month
            today   - show the date for today
            weeks   - list the Mondays for N weeks
        ''')


# ------------------------------
# Functions

# Convert from a time record to string
def date_str(t):
    return t.strftime("%Y-%m-%d")


# Format like   Tue, 03-11
def day_str(t):
    return t.strftime("%a, %m-%d")


# Return a date from 48 hours ago
def days_ago(date,days):
    return  date_str(date-timedelta(days=days))


# Day of the week
def day_name(year, month, day):
    return day_abbr[weekday(year, month, day)]


# Calculate the days I've lived
def my_age_in_days():
    birth_date = to_date('1959-09-01')
    today = datetime.now()
    days = today - birth_date
    return days.days


# Enumerate days for the previous week
def days_list(args):
    if args:
        days = int(args[0])
    else:
        days = 7
    if args[1:]:
        today = to_date(args[1])
    else:
        today = datetime.today()

    print('Days: %d, To: %s'%(days,day_str(today)))

    for d in enumerate_days(today, days):
        print(day_str(to_date(d)))


#  days of this month
def days_month(args):
    start = datetime.today() + timedelta(days=31 - datetime.today().day)
    for d in enumerate_days(start, 31):
        print(d)


# Save the Mondays in a file for some number of weeks
def days_weeks(start, num_weeks):

    def days_ahead(date, days):
        day = date + timedelta(days=days)
        return day

    def enumerate_weeks(today, days):
        x = []
        for d in range(days):
            day = days_ahead(today, d)
            if day.weekday() == 0:
                x.append(day_str(day))
        return x

    def weekly_schedule(days):
        start = '2019-04-29'
        for i, d in enumerate(enumerate_weeks(to_date(start), days)):
            print('Week %s - %s\n' % (i+1, d))

    weekly_schedule(int(num_weeks)*7)


# List all of the days before today
def enumerate_days(today, days):
    return [days_ago(today, days-d-1) for d in range(days)]


# List all the days in the month
def enumerate_month(year, month):
    # print("\n\n%s %s\n" % (month_name[month], year))
    num_days = monthrange(year, month)[1]
    return ['%04d-%02d-%02d' % (year, month, d + 1) for d in range(num_days)]


# # List all the days in the month
# def enumerate_month_days(year, month):
#     num_days = monthrange(year, month)[1]
#     return [for d in range(num_days)]
#         x = ' %s, %04d-%02d-%02d' % (day_name(year, month, d + 1), year, month, d + 1)
#         print(x)


# Convert from string to ctime object  (example format 1959-09-01)
def to_date(s):
    return datetime.strptime(s, "%Y-%m-%d")


# Convert from string to ctime object (example format 9/1/1959)
def parse_date(s):
    return datetime.strptime(s, "%m/%d/%Y")


# Convert from string to ctime object  (example format Tue, 09-01)
def to_day(s):
    return datetime.strptime(s, "%a, %m-%d")


# Today's date as string
def today():
    return date_str(datetime.now())


# Show a list of dates for the last month
def print_recent_dates():
    for d in enumerate_days(to_date(today()), 90):
        print('* [%s](/info/history/%s) - Write - ' % (d, d.replace('-', '/')))


# Convert a string to a timezone aware date
def due_date(due):
    return make_aware(datetime.strptime(due, "%Y-%m-%d"))

