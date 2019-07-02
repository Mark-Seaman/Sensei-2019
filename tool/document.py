from os import mkdir, listdir
from os.path import exists, isdir, isfile, join, dirname
from platform import node

from tool.shell import read_file, shell_pipe
from hammer.settings import BASE_DIR
from tool.log import log


def doc_cards(page):
    if doc_exists(page):
        text = doc_content(page)
    else:
        text = 'No Document found, %s' % page
    text = text.split('\n## ')
    results = []
    for i, t in enumerate(text):
        t = t.split('\n')
        title = t[0]
        body = '\n'.join(t[1:])
        body = text_to_html(body)
        results.append((title, body))
    return results


def doc_content(page):
    return read_file(doc_path(page))


def doc_dir_exists(title):
    log('doc_dir_exists', title)
    path = doc_path(title)
    return isdir(path)


def doc_exists(title):
    # log('doc_exists', title)
    path = doc_path(title)
    if exists(path) and isfile(path):
        return path
    elif exists(path + '.md'):
        return path + '.md'
    elif isdir(path) and exists(join(path, 'Index')):
        return join(path, 'Index')
    elif isdir(path) and exists(join(path, 'Index.md')):
        return join(path, 'Index.md')


def doc_html_text(page, image_path=None):
    doc = doc_exists(page)
    if not doc:
        # from django.http import Http404
        # raise Http404("DocDisplay - Document does not exist")
        return "<h1>Missing Document</h1><p>We are sorry, but the document you were looking for could not be found.</p>"
    return file_to_html(doc, image_path)


def doc_link(title):
    return title.replace('.md', '')


def doc_list(docdir):
    files = listdir(doc_path(docdir))
    return [(('%s/%s' % (docdir,f)), (title(doc_path('%s/%s') % (docdir,f)))) for f in files]


def doc_file_index(docdir):
    files = listdir(doc_path(docdir))
    return [(('%s/%s' % (docdir,f)), '%s' % f) for f in files]


def doc_page(title):
    log('doc_page', title)
    path = doc_path(title)
    if exists(path) and isfile(path):
        # log('no redirect')
        return None
    elif exists(path + '.md'):
        log('MD redirect')
        return title + '.md'
    elif isdir(path) and exists(join(path, 'Index')):
        log('Index redirect')
        return join(title, 'Index')
    elif isdir(path) and exists(join(path, 'Index.md')):
        log('Index.md redirect')
        return join(title, 'Index.md')
    else:
        log('Missing document '+title)
        return None


def doc_path(page):
    return join(BASE_DIR, 'Documents', page)


def doc_title(page):
    doc = doc_path(page)
    if not exists(doc):
        return 'Doc not found, ' + doc
    return title(doc)


def domain_doc(domain, page):
    if domain == 'spiritual-things.org':
        d = 'spiritual'
    elif domain == 'markseaman.org':
        d = 'MarkSeaman'
    elif domain == 'markseaman.info':
        d = 'info'
    elif domain == 'seamanslog.com':
        d = 'seamanslog'
    elif domain == 'seamansguide.com':
        d = 'guide'
    elif domain == 'shrinking-world.com':
        d = 'shrinkingworld'
    else:
        return page

    if page.startswith(d):
        return page
    else:
        return join(d, page)


def file_to_html(path, image_path=None):
    def fix_images(text):
        return text.replace('](img/', '](%s/' % image_path)

    if exists(path):
        return text_to_html(fix_images(read_markdown(path)))
    else:
        return 'No file found, ' + path


def markdown_to_html(markdown_path, html_path):
    text = read_markdown(markdown_path)
    text = text_to_html(text)
    write_html_file(html_path, text)


def read_markdown(path):
    try:
        bad_files = ['.DS_Store', '.jpg', '.jpeg', '.png', '.gif']
        for x in bad_files:
            if x in path:
                return "No Markdown File: " + path
        return open(path).read()
    except:
        print('Found bad document: %s' % path)
        return 'Found bad document: %s' % path


def text_to_html(text):
    if 'MCB15-3365' == node():
        PANDOC_APP = 'pandoc.exe'
    elif 'Marks-iMac.local' == node():
        PANDOC_APP = '/usr/local/bin/pandoc'
    elif 'seaman-macbook.local' == node():
        PANDOC_APP = '/usr/local/bin/pandoc'
    else:
        PANDOC_APP = 'pandoc'
    return shell_pipe(PANDOC_APP, text)


def title(p1):
    return open(p1).read().split('\n')[0][2:]


def write_html_file(path, html):
    if not exists(dirname(path)):
        mkdir(dirname(path))
    open(path, 'w').write(html)
