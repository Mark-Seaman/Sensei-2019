from re import search

from tool.files import read_text
from tool.shell import shell_script
from tool.text import delete_lines, text_replace, text_lines, text_join


def redact_css(text):
    match = '\.css\?.*/n'
    replacement = 'css/n'
    return text_replace(text, match, replacement)


def code_files():
    text = shell_script('find . -name "*.py"|grep -v /env')
    return text_lines(text)


def code_search(words):
    return file_search(code_files(), words)


def file_search(files, words):
    matches = []
    for f in files:
        text = text_lines(read_text(f))
        for pattern in words:
            text = [('%s: %s' % (f, line)) for line in text if search(pattern, line)]
        if text:
            matches += text
    return text_join(matches)


def html_files():
    text = shell_script('find . -name "*.html"') + '\n' + shell_script('find . -name "*.css"')
    return text_lines(delete_lines(text, 'min.css'))


def html_search(words):
    files = html_files()
    return file_search(files, words)


def doc_files():
    text = shell_script('find Documents -type f|grep -v /.git' )
    return text_lines(delete_lines(delete_lines(text, 'info'), '.DS_Store'))


def doc_search(words):
    files = doc_files()
    return file_search(files, words)


def text_search(words):
    files = code_files() + html_files() + doc_files()
    return file_search(files, words)
