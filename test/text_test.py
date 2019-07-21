from test.text import redact_css, code_files, code_search, doc_search, html_search
from tool.text import text_replace


def text_replace_test():
    return text_replace('Four score and seven years', 'score', 'generations')


def text_code_files_test():
    return '\n'.join(code_files())


def text_code_search_test():
    return code_search(['def ', 'module'])


def text_css_filter_test():
    text = 'href="/static/css/guide.css?time=July 4, 2019, 8:42 a.m."/nOutput this'
    return redact_css(text)


def text_html_search_test():
    return html_search(['h1'])


def text_doc_search_test():
    text = doc_search(['Seaman','shrinkingworld'])
    return text
