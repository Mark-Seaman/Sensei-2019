from tool.text import text_replace


def text_files_test():
    return text_replace('Four score and seven years', 'score', 'generations')


def text_css_filter_test():
    text = 'href="/static/css/guide.css?time=July 4, 2019, 8:42 a.m."/nOutput this'
    match = '\.css\?.*/n'
    replacement = 'css/n'
    return text_replace(text, match, replacement)
