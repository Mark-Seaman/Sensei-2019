from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from tool.document import doc_file_index, doc_list
from tool.log import log_page

from .mybook import *
from .views import DocDisplay


class BookNotes(DocDisplay):
    template_name = 'mybook_theme.html'
    site_title = 'Book Notes', 'Growth through reading'
    logo = "/static/images/MarkSeaman.100.png", 'Mark Seaman'

    def get_content_data(self):
        excerpt, url = booknotes_excerpt(self.kwargs.get('title'))
        self.text = dict(title=self.title, text=excerpt, readmore=(url, url), excerpt=excerpt)
        self.menu = mark_seaman_menu(self.title)


class Leverage(DocDisplay):
    site_title = 'Software Engineering', 'Best Practices of Software Development'
    logo = "/static/images/SWS_Logo_200.jpg", 'Shrinking World Solutions'

    def get_content_data(self):
        self.text = document_text(domain_doc(self.domain, self.title))
        self.menu = leverage_menu(self.kwargs.get('title', 'Index'))


class MarkSeaman(DocDisplay):
    site_title = 'Mark Seaman', 'Inventor - Teacher - Writer'
    logo = "/static/images/MarkSeaman.100.png", 'Mark Seaman'

    def get_content_data(self):
        domain = self.request.get_host()
        self.title = self.request.path[1:]
        self.text = document_text(domain_doc(domain,self.title))
        self.menu = mark_seaman_menu(self.title)


class PrivateDoc(LoginRequiredMixin, DocDisplay):
    template_name = 'task_theme.html'
    site_title = "My Brain", 'Top Secret Notes'
    logo = "/static/images/SWS_Logo_200.jpg", 'Shrinking World Solutions'

    def get_content_data(self):
        self.domain = self.request.get_host()
        self.title = self.kwargs.get('title', 'Index')
        self.menu = info_menu(self.title)
        self.text = document_text(domain_doc(self.domain, self.request.path[1:]))


def seamans_log_menu(title):
    def menu_items(title):
        return [('List', 'Articles', title == 'Index'),
                ('Random', 'Read', title != 'List' and title != 'Index'),
                ('https://markseaman.org', 'Mark Seaman')]

    return topic_menu(menu_items(title), '/seamanslog/', "Seaman's Log")


class SeamansLog(DocDisplay):

    def get_context_data(self, **kwargs):

        def logo():
            return "/static/images/MarkSeaman.100.png", 'Mark Seaman'

        domain = self.request.get_host()
        title = self.kwargs.get('title', 'Index')
        site_title = "Seaman's Log", 'Big Ideas & Deep Thoughts'
        text = page_text(domain, self.request.path[1:])
        menu = seamans_log_menu(title)
        return page_settings(title, site_title, logo(), menu, text['text'], text['url'])


class DocFileIndex(TemplateView):
    template_name = 'mybook_list.html'

    def get_context_data(self, **kwargs):
        log_page(self.request)
        title = self.request.path[1:-6]
        site_title = "Shrinking World", 'Software Development Training'
        logo = "/static/images/SWS_Logo_200.jpg", 'Shrinking World Solutions'
        menu = seamans_log_menu(title)
        settings = page_settings(title, site_title, logo, menu, 'no text')
        settings['list'] = doc_file_index(title)
        return settings


class DocList(TemplateView):
    template_name = 'mybook_list.html'

    def get_context_data(self, **kwargs):
        log_page(self.request)
        title = self.request.path[1:-5]
        site_title = "Shrinking World", 'Software Development Training'
        logo = "/static/images/SWS_Logo_200.jpg", 'Shrinking World Solutions'
        menu = seamans_log_menu(title)
        settings = page_settings(title, site_title, logo, menu, 'no text')
        settings['list'] = doc_list(title)
        return settings

