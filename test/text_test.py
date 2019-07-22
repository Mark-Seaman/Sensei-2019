from tool.text import text_join, text_replace
from tool.code import  doc_files, doc_search


def text_doc_files_test():
    return text_join(doc_files())


def text_replace_test():
    return text_replace('Four score and seven years', 'score', 'generations')

