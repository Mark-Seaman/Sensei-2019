from re import search

from tool.files import read_text
from tool.shell import shell_script
from tool.text import text_replace, text_lines, text_join


def redact_css(text):
    match = '\.css\?.*/n'
    replacement = 'css/n'
    return text_replace(text, match, replacement)


def code_files():
    text = shell_script('find . -name "*.py"')
    return text_lines(text)


def file_search(files, words):
    matches = []
    for f in files:
        text = text_lines(read_text(f))
        for pattern in words:
            text = [line for line in text if search(pattern, line)]
        if text:
            matches += text
    return text_join(matches)


def code_search(words):
    return file_search(code_files(), words)


def html_search(words):
    word = words[0]
    files = 'Documents'
    text = shell_script('grep %s -r  %s' % (word, files))
    return text


def doc_search(words):
    word = words[0]
    files = 'Documents'
    text = shell_script('grep %s -r  %s' % (word, files))
    return text


def text_search(text, words):
    return text