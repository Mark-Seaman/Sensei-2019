from tool.text import text_join, text_replace, doc_files, doc_search
from tool.code import code_files, code_search, text_search, html_files, html_search
from tool.shell import redact_css




def text_doc_files_test():
    return text_join(doc_files())


def text_doc_search_test():
    # return text_search(['h1'])

    text = doc_search(['Seaman','shrinkingworld'])
    return text


def text_replace_test():
    return text_replace('Four score and seven years', 'score', 'generations')

