from tool.shell import shell_script


def app_code_search_test():
    word = 'django'
    files = '$p/*/*.py'
    return shell_script('grep %s %s|wc -l' % (word, files))


def app_template_search_test():
    word = 'h2'
    files = '$p/*/templates/*.html'
    return shell_script('grep %s  %s|wc -l' % (word, files))


def app_doc_search_test():
    word = 'Seaman'
    files = 'Documents'
    return shell_script('grep %s -r  %s|grep -v .git|wc -l' % (word, files))

