from django.contrib.auth.models import User

from tool.text import text_join


def add_user_login(name, email, password='student'):
    assert ' ' in name
    first = name.split(' ')[0]
    last = ' '.join(name.split(' ')[1:])
    username = email[:email.index('@')].replace('mark.b.seaman+', '')

    u = User.objects.get_or_create(username=username)[0]
    u.first_name = first
    u.last_name = last
    u.email = email
    u.is_staff = True
    u.set_password(password)
    u.save()
    return u


def list_user_login(user):
    name = user.first_name + ' ' + user.last_name
    return '%-2d %-20s %-20s %-30s ' % (user.pk, name, user.username, user.email)


def list_users():
    return text_join([list_user_login(u) for u in User.objects.all()])

