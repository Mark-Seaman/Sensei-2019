
from .mybook import  page_settings, page_text, topic_menu
from .views import DocDisplay


def guide_menu(page, title):

    def sws_items():
        return [('https://shrinking-world.com', 'Shrinking World'),
                ('https://shrinking-world.com/unc/', 'UNC Courses'),
                ('https://shrinking-world.com/shrinkingworld/Leverage', 'Leverage'),
                ('https://markseaman.org', 'Mark Seaman')]

    return topic_menu(sws_items(), '', title)


def lifecycle_menu(page, title):

    def lifecycle_items(page):
        return [('Requirements', 'Requirements', 'Requirements' in page),
                ('Design', 'Design', 'Design' in page),
                ('Code', 'Code', 'Code' in page),
                ('Test', 'Test',  'Test' in page)]

    return topic_menu(lifecycle_items(page), '', title)


def guide_settings(title):
    logo = "/static/images/SWS_Globe_small.jpg", 'Mark Seaman'
    if title.startswith('guide/Software'):
        site_title = "Software Engineering", 'Principles and Practices'
        menu = lifecycle_menu(title, "Software Engineering")
        return site_title, menu,logo
    elif title.startswith('guide/PhpApps'):
        site_title = "PHP Apps", 'Software Engineering Cookbook'
        menu =  lifecycle_menu(title, "PHP Apps")
        return site_title, menu,logo
    elif title.startswith('guide/PythonApps'):
        site_title = "Python Apps", 'Software Engineering Cookbook'
        menu =  lifecycle_menu(title, "Python Apps")
        return site_title, menu,logo
    elif title.startswith('guide/HtmlApps'):
        site_title = "HTML Apps", 'Software Engineering Cookbook'
        menu =  lifecycle_menu(title, "HTML Apps")
        return site_title, menu,logo
    else:
        site_title = "Seaman's Guides", 'Software Development Training'
        menu =  guide_menu(title, "Seaman's Guides")
        return site_title,menu,logo


class SeamansGuide(DocDisplay):

    def get_context_data(self, **kwargs):
        domain = self.request.get_host()
        title = self.request.path[1:]
        site_title,menu,logo = guide_settings(title)
        text = page_text(domain, title)
        return page_settings(title, site_title, logo, menu, text['text'], text['url'])
