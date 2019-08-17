from re import findall

from tool.shell import shell_file_list
from tool.text import delete_lines, file_search, match_pattern, text_lines, text_join, transform_matches


def code_files(path='.'):
    exclude = ['env', '.venv']
    files = shell_file_list(path, 'py', exclude)
    files = delete_lines(files, '.DS_Store')
    return text_lines(files)


def doc_files():
    exclude = ['.git', 'env', '.venv']
    files = shell_file_list('Documents', '', exclude)
    files = delete_lines(files, '.DS_Store')
    files = delete_lines(files, 'dktht')
    return text_lines(files)


# def doc_search(words):
#     files = doc_files()
#     return file_search(files, words)


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
    exclude = ['env', '.venv']
    files = text_lines(shell_file_list('.', 'html', exclude))
    files += text_lines(shell_file_list('.', 'css', exclude))
    return files


# def html_search(words):
#     files = html_files()
#     return file_search(files, words)
#

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


def text_search(args):
    selector = args[0]
    words = args[1:]
    if selector == 'code':
        files = code_files()
    elif selector == 'doc':
        files = doc_files()
    elif selector == 'html':
        files = html_files()
    else:
        files = code_files() + html_files() + doc_files()
    # print(selector + 'search:')
    return file_search(files, words)

