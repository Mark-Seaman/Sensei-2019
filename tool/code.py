from re import findall

from tool.shell import shell_script, shell_file_list
from tool.text import delete_lines, file_search, match_pattern, text_lines, text_join, transform_matches


def code_files(path='.'):
    files = shell_script('find %s -name "*.py"|grep -v /env/|grep -v .venv/' % path)
    files = text_lines(files)
    return [f for f in files if f]


def code_search(path, words):
    return file_search(code_files(path), words)


def doc_files():
    exclude = ['.git', 'info', 'spiritual']
    files = shell_file_list('Documents', exclude)
    files = delete_lines(files, '.DS_Store')
    return files.split('\n')


def doc_search(words):
    files = doc_files()
    return file_search(files, words)


def find_classes(text):
    pattern = r'class (.*)\(.*\)'
    return match_pattern(text, pattern).split('\n')


def find_functions(text):
    pattern = r'\ndef (.*)\(.*\)'
    return findall(pattern, text)


def find_signatures(text):
    pattern = r'def(.*\(.*\)):'
    return transform_matches(text, pattern, r'\1').split('\n')


def html_files():
    html_files = shell_script('find . -name "*.html"|grep -v /env/| grep -v .venv/')
    css_files = shell_script('find . -name "*.css"|grep -v /env/| grep -v .venv/|grep -v min.css')
    files = html_files + '\n' + css_files
    return text_lines(files)


def html_search(words):
    files = html_files()
    return file_search(files, words)


def list_functions():
    functions = []
    files = code_files()
    for code in files:
        text = open(code).read()
        functions.append(code + ':')
        functions.append('    ' + '\n    '.join(find_functions(text)))
    return text_join(functions)


def source_code():
    return '\n'.join([open(code).read() for code in code_files()])


def text_search(words):
    files = code_files() + html_files() + doc_files()
    return file_search(files, words)


