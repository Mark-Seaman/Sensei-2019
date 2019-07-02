from django.http import HttpResponseRedirect
from django.views.generic import RedirectView, TemplateView
from os import listdir
from os.path import join
from random import choice

from tool.document import doc_page, domain_doc
from tool.log import log, log_page

from mybook.mybook import shrinking_world_menu
from mybook.mybook import document_text, page_settings


class DocDisplay(TemplateView):
    template_name = 'seaman_theme.html'
    site_title = "Shrinking World", 'Software Development Training'
    logo = "/static/images/SWS_Logo_200.jpg", 'Shrinking World Solutions'

    def get_content_data(self):
        self.text = document_text(domain_doc(self.domain, self.title))
        self.menu = shrinking_world_menu(self.title)

    def get_context_data(self, **kwargs):
        log_page(self.request)
        self.domain = self.request.get_host()
        self.title = self.request.path[1:]
        self.get_content_data()
        return page_settings(self.title, self.site_title, self.logo, self.menu, self.text)

    def get(self, request, *args, **kwargs):
        title = self.kwargs.get('title', 'Index')
        url = doc_page(self.request.path[1:])
        if url:
            log('REDIRECT: %s --> %s' % (title, url))
            return HttpResponseRedirect('/' + url)

        return self.render_to_response(self.get_context_data(**kwargs))


class DocMissing(TemplateView):
    template_name = 'mybook_missing.html'

    def get_context_data(self, **kwargs):
        title = self.request.path[1:]
        site_title = "Shrinking World", 'Software Development Training'
        logo = "/static/images/SWS_Logo_200.jpg", 'Shrinking World Solutions'
        settings = page_settings(title, site_title, logo, shrinking_world_menu(title), 'missing doc')
        return settings


class DocRandom(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        title = self.kwargs.get('title')
        files = listdir(join('Documents', title))
        file = choice(files)
        return '/%s/%s' % (title, file)


class DocRoot(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        log_page(self.request, 'Redirect Index')
        return '/%s' % domain_doc(self.request.get_host(),'Index')
