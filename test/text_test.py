from tool.text import delete_lines, text_join, text_replace
from tool.code import doc_files
from tool.shell import no_blank_lines


def text_doc_files_test():
    return text_join(doc_files())


def text_replace_test():
    return text_replace('Four score and seven years', 'score', 'generations')


def text_blank_lines_test():
    text = '''
    Apples
    
    Bananas
    
    Carrots
    '''
    return no_blank_lines(text)


def text_delete_lines_test():
    text = '''
        Apples

        Bananas

        Carrots
        '''
    return delete_lines(text, 'Bananas')

