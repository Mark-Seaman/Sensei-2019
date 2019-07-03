from tool.shell import curl_get


def brain_curl_test():
    return curl_get('localhost:8000/static/css/brain.css')


def brain_page_test():
    return curl_get('localhost:8000/brain/Index')


def brain_sws_page_test():
    return curl_get('https://shrinking-world.com/Index')


def brain_mso_page_test():
    return curl_get('https://MarkSeaman.org/Index')


def brain_missing_page_test():
    return curl_get('https://MarkSeaman.org/xxx')


def brain_localhost_pages_test():
    pages = '''
brain/Index
MarkSeaman/Index
info/Index
    '''.split('\n')[1:-1]
    output = [curl_get('localhost:8000/%s' % p) for p in pages]
    return '\n'.join(output)


def brain_web_pages_test():
    pages = '''
https://shrinking-world.com/Index
https://MarkSeaman.org/Index
https://MarkSeaman.info/info/Index
    '''.split('\n')[1:-1]
    output = [curl_get(p) for p in pages]
    return '\n'.join(output)
