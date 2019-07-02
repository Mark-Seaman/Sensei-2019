from django.utils.timezone import now
from os import listdir
from os.path import join
from random import choice

from bin.shell import read_file
from hammer.settings import BASE_DIR
from tool.document import doc_title, text_to_html, domain_doc, doc_html_text
from tool.log import log


def booknotes_excerpt(doc):

    def booknotes_doc_path(doc=None):
        path = join(BASE_DIR, 'Documents', 'MarkSeaman', 'booknotes')
        if doc:
            path = join(path, doc)
        return path

    def booknotes(doc):
        if not doc:
            not_these = ['Index', 'Menu', 'SiteTitle']
            notes = [b for b in listdir(booknotes_doc_path()) if b not in not_these]
            doc = choice(notes)
        return doc

    def excerpt(note):
        path = booknotes_doc_path(note)
        text = read_file(path).split('\n\n## Excerpts\n\n')
        if text[1:]:
            excerpts = text[1].split('\n\n')
            excerpts = [e for e in excerpts if e and e!='\n']
            excerpt = choice(excerpts).replace('\n',' ')
            log('Booknotes - %s: %s' % (path, excerpt))
            excerpt = '\n\n## Excerpt\n\n'+excerpt
        else:
            excerpt = ''
        summary = text[0]
        return text_to_html(summary + excerpt)

    doc = booknotes(doc)
    return excerpt(doc), 'http://markseaman.org/MarkSeaman/booknotes/%s' % doc


def document_text(title):
    return doc_html_text(title, '/static/images')


def page_settings(title, site_title, logo=None, menu=None, text=None, url=None):
    if logo:
        header = dict(title=site_title[0], subtitle=site_title[1], logo=logo[0], logo_text=logo[1])
    else:
        header = dict(title=site_title[0], subtitle=site_title[1])
    time = now()
    return dict(title=title, menu=menu, header=header, text=text, url=url, time=time)


def page_hyperlink(domain, title):
    domdoc = domain_doc(domain, title)
    return "http://%s/%s" % (domain, domdoc)


def page_doc(title):
    return title.split('/')[-1]


def page_text(domain, title):
    text = doc_html_text(title, '/static/images')
    doc = page_doc(title)
    url = page_hyperlink(domain, title)
    title = doc_title(title)
    return dict(doc=doc, title=title, text=text, url=url)


def topic_menu(topics, base, home, href='/'):

    def is_active(active):
        return ' active' if active and active[0] else ''

    def menu_url (base, page):
        if page.startswith('http'):
            return page
        else:
            return base + page

    menu_items = [dict(url=menu_url(base, i[0]), label=i[1], active=is_active(i[2:])) for i in topics]
    return (home,href), menu_items


def shrinking_world_menu(title):
    def menu_items(title):
        return [('https://shrinking-world.com', 'Shrinking World', title == 'Index'),
                ('https://shrinking-world.com/shrinkingworld/Leverage/', 'Leverage'),
                ('https://seamansguide.com', 'Guides'),
                ('https://seamanslog.com', 'Blog'),
                ('https://markseaman.org', 'Mark Seaman')]

    return topic_menu(menu_items(title), '/shrinkingworld/', "Shrinking World")


def leverage_menu(title):

    def menu_items(title):
        return [('Part1', 'Leverage', title == 'Part1'),
                ('Part2', 'Development', title == 'Part2'),
                ('Part3', 'Operations', title == 'Part3'),
                ('Part4', 'Teams', title == 'Part4')]

    return topic_menu(menu_items(title), '/shrinkingworld/Leverage/', "Leverage Principle", 'Index')


def info_menu(title):

    def menu_items(title):
        return [('Past', 'Past', title == 'Past.md'),
                ('Index', 'Present', title == 'Index.md'),
                ('Future', 'Future', title == 'Future.md'),
                ('https://shrinking-world.com', 'Shrinking World'),
                ('https://markseaman.org', 'Mark Seaman')]

    return topic_menu(menu_items(title), '/info/', "Brain")


def mark_seaman_menu(title):
    def menu_items(title):
        return [('https://seamanslog.com', 'Blog'),
                ('https://shrinking-world.com', 'Shrinking World'),
                ('https://markseaman.org', 'Mark Seaman', True)]
    return topic_menu(menu_items(title), '/MarkSeaman/', "Mark Seaman")
