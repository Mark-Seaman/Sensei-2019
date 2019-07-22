from tool.text import text_join, text_lines
from tool.code import code_files, code_search, doc_files, doc_search, source_code, text_search, html_files, html_search, list_functions
from tool.shell import redact_css


def code_css_filter_test():
    text = '<link href="/static/css/guide.css?time=July 4, 2019, 8:42 a.m.">\nOutput this'
    return redact_css(text)


def code_doc_files_test():
    return text_join(doc_files())


def code_doc_search_test():
    text = doc_search(['Seaman','shrinkingworld'])
    return text


def code_files_test():
    return text_join(code_files('tool') + code_files('mybook'))


def code_functions_test():
    return list_functions()


def code_html_files_test():
    return text_join(html_files())


def code_html_search_test():
    return html_search(['h1'])


def code_search_test():
    return text_search(['h1'])


def code_search_test():
    return code_search('tool', ['def '])


# def code_search2_test():
#     return text_search(['def ', 'module'])


def code_source_test():
    files = len(code_files())
    source = len(text_lines(source_code()))
    functions = len(text_lines(list_functions()))
    return '%s files, %s functions, %s lines of source code' % (files, functions, source)


