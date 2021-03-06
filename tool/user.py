from django.contrib.auth.models import User

from tool.text import text_join


def add_user_login(first, last, email, password='student'):
    username = email[:email.index('@')].replace('mark.b.seaman+', '')

    u = User.objects.get_or_create(username=username)[0]
    u.first_name = first
    u.last_name = last
    u.email = email
    u.is_staff = True
    u.set_password(password)
    u.save()
    return u


def change_password(username, password):
    u = User.objects.get(username=username)
    u.set_password(password)
    u.save()


def list_user_login(user):
    name = user.first_name + ' ' + user.last_name
    return '%-2d %-30s %-20s %-30s ' % (user.pk, name, user.username, user.email)


def list_users():
    return text_join([list_user_login(u) for u in User.objects.all()])

