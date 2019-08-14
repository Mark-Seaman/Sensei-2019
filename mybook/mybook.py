from django.utils.timezone import now
from os import listdir
from os.path import join
from random import choice
from re import findall

from tool.shell import read_file
from hammer.settings import BASE_DIR
from tool.days import my_age_in_days
from tool.document import doc_title, text_to_html, domain_doc, doc_html_text, read_markdown, doc_path
from tool.log import log
from tool.text import find_markdown_links


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


def get_extra_data(title, text):
    if title == 'info/Write/Think/Creativity.md':
        # summary = get_link_summary(title)
        # return dict(card=dict(title='Hyperlinks', text=summary))
        summary = get_task_summary(title)
        return dict(card=dict(title='Task Types', text=summary))
    if title.startswith('info'):
        return dict(day=my_age_in_days())


def get_link_summary(title):
    text = read_markdown(doc_path(title))
    return find_markdown_links(text)


def get_task_summary(title):
    text = read_markdown(doc_path(title))
    match_pattern = r'\[.*\]\(.*\) *\- (\w*) \- '
    tasks = {}
    for match in findall(match_pattern, text):
        tasks.setdefault(match, 0)
        tasks[match] = tasks[match] + 1
    tasks = sorted(tasks.items(), key=lambda t: (t[1], t[0]), reverse=True)
    return '\n'.join(['%s: %s' % (t[0], t[1]) for t in tasks])


def page_doc(title):
    return title.split('/')[-1]


def page_hyperlink(domain, title):
    domdoc = domain_doc(domain, title)
    return "http://%s/%s" % (domain, domdoc)


def page_settings(title, site_title, logo=None, menu=None, text=None, data=None):
    if logo:
        header = dict(title=site_title[0], subtitle=site_title[1], logo=logo[0], logo_text=logo[1])
    else:
        header = dict(title=site_title[0], subtitle=site_title[1])
    time = now()
    return dict(title=title, menu=menu, header=header, text=text, data=data, time=time)


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


def unc_menu(course, title):

    def homework_menu(title):

        def menu_items(title):
            return [('Part1', 'HTML', title == 'Part1'),
                    ('Part2', 'CSS', title == 'Part2'),
                    ('Part3', 'Design', title == 'Part3')]
        return topic_menu(menu_items(title), '/unc/bacs200', "BACS 200", 'Index')

    def bacs_350_menu(title):
        def menu_items(title):
            return [('Part1', 'Views',  title == 'Part1'),
                    ('Part2', 'Data',   title == 'Part2'),
                    ('Part3', 'Design', title == 'Part3')]
        return topic_menu(menu_items(title), '/unc/bacs350', "BACS 350", 'Index')

    if course == 'bacs200':
        return homework_menu(title)
    elif course == 'bacs350':
        return bacs_350_menu(title)


def mark_seaman_menu(title):
    def menu_items(title):
        return [('https://seamanslog.com', 'Blog'),
                ('https://shrinking-world.com', 'Shrinking World'),
                ('https://markseaman.org', 'Mark Seaman', True)]
    return topic_menu(menu_items(title), '/MarkSeaman/', "Mark Seaman")


def seamans_log_menu(title):
    def menu_items(title):
        return [('List', 'Articles', title == 'Index'),
                ('Random', 'Read', title != 'List' and title != 'Index'),
                ('https://markseaman.org', 'Mark Seaman')]

    return topic_menu(menu_items(title), '/seamanslog/', "Seaman's Log")


def shrinking_world_menu(title):
    def menu_items(title):
        return [('https://shrinking-world.com', 'Shrinking World', title == 'Index'),
                ('https://shrinking-world.com/shrinkingworld/Leverage/', 'Leverage'),
                ('https://seamansguide.com', 'Guides'),
                ('https://seamanslog.com', 'Blog'),
                ('https://markseaman.org', 'Mark Seaman')]

    return topic_menu(menu_items(title), '/shrinkingworld/', "Shrinking World")


