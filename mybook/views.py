from django.http import HttpResponseRedirect
from django.views.generic import RedirectView, TemplateView
from os import listdir
from os.path import join
from random import choice

from mybook.mybook import shrinking_world_menu, read_system_log
from mybook.mybook import document_text, page_settings
from tool.document import doc_page, domain_doc
from tool.log import log, log_page
from unc.models import Student


class SeamanFamily(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        return 'https://seamanfamily.org/%s' % self.kwargs.get('title')


class SystemLog(TemplateView):
    template_name = 'mybook_log.html'

    def get_context_data(self, **kwargs):
        log_page(self.request)
        kwargs['history'] = read_system_log()
        header = 'Sensei Server', 'System Log', "/static/images/SWS_Logo_200.jpg", 'Shrinking World Solutions'
        kwargs['header'] = dict(title=header[0], subtitle=header[1], logo=header[2], logo_text=header[3])
        return kwargs


class DocDisplay(TemplateView):
    template_name = 'mybook_theme.html'
    site_title = "Shrinking World", 'Software Development Training'
    logo = "/static/images/SWS_Logo_200.jpg", 'Shrinking World Solutions'
    data = {}

    def get_content_data(self):
        self.text = document_text(domain_doc(self.domain, self.title))
        self.menu = shrinking_world_menu(self.title)

    def get_context_data(self, **kwargs):
        log_page(self.request)
        self.domain = self.request.get_host()
        self.title = self.request.path[1:]
        self.get_content_data()
        return page_settings(self.title, self.site_title, self.logo, self.menu, self.text, self.data)

    def get(self, request, *args, **kwargs):
        path = self.request.path[1:]
        log("GET: path = %s" % path)
        log('USER: user = %s' % self.request.user.username)
        if path.startswith('info'):
            if not self.request.user.is_superuser:
                redir = 'https://shrinking-world.com/shrinkingworld/SecurityViolation'
                log('SECURITY VIOLATION: %s --> %s' % (path, redir))
                return HttpResponseRedirect(redir)
        url = doc_page(path)
        if url:
            log('REDIRECT: %s --> %s' % (path, url))
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
        u = self.request.user
        if not u.is_anonymous:
            s = Student.objects.filter(user=u)
            if s:
                return '/unc/%s' % s[0].course.name
        return '/%s' % domain_doc(self.request.get_host(), 'Index')
