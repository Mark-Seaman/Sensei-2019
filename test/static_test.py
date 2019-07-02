from tool.files import recursive_list
from tool.shell import curl_get


def static_curl_test():
    return curl_get('https://seamanfamily.org/static/css/brain.css')


def static_files_test():
    files = [f for f in recursive_list('static')]
    return '\n'.join(files)
