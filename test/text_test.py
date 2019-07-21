from test.text import redact_css, code_files, code_search
from tool.text import count_lines, delete_lines, text_replace


def text_replace_test():
    return text_replace('Four score and seven years', 'score', 'generations')


def text_code_files_test():
    return '\n'.join(code_files())


def text_code_search_test():
    return code_search(['def ', 'module'])


def text_css_filter_test():
    text = 'href="/static/css/guide.css?time=July 4, 2019, 8:42 a.m."/nOutput this'
    return redact_css(text)


def text_search_test():
    text = code_search(['Seaman'])
    return count_lines(delete_lines(delete_lines(delete_lines(text, '.git'), 'info'), 'unc'))

