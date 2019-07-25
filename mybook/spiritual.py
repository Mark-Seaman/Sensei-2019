from django.views.generic import RedirectView
from os import listdir
from os.path import join
from random import choice

from .views import DocDisplay
from .mybook import topic_menu, page_text


def spiritual_menu(title):
    def spiritual_topics():
        return [('Index', 'Home', title.startswith('Index')),
                ('reflect', 'Reflect', title.startswith('reflect')),
                ('bible', 'Meditate', title.startswith('bible')),
                ('teaching', 'Learn', title.startswith('teaching')),
                ('walkabout', 'Journey', title.startswith('walkabout')),
                ('prayers', 'Pray', title.startswith('prayers'))]

    return topic_menu(spiritual_topics(), '/spiritual/', "Spiritual Things")


def select_random_document(title):
    if not title:
        title = choice(['reflect', 'teaching', 'prayers', 'bible', 'walkabout'])
    files = listdir(join('Documents', 'spiritual', title))
    file = choice(files)
    return '/spiritual/%s/%s' % (title, file)


class SpiritualDoc(DocDisplay):
    template_name = 'spiritual_theme.html'
    site_title = 'Spiritual Things', 'Daily Inspiration'
    logo = None

    def get_content_data(self):
        self.text = page_text(self.domain, self.title)
        self.menu = spiritual_menu(self.kwargs.get('title','Index'))


class SpiritualSelect(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        title = kwargs.get('title')
        return select_random_document(title)


