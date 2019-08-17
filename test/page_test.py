
from tool.page import close_browser_dom, open_browser_dom
from tool.shell import curl_get, is_server


def page_curl_test():
    pages = '''
https://shrinking-world.com/Index
https://MarkSeaman.org/Index
https://MarkSeaman.info/info/Index
    '''.split('\n')[1:-1]
    output = [curl_get(p) for p in pages]
    return '\n'.join(output)


def page_features_test():
    if is_server():
        return 'No Selenium on Sensei Server'
    else:
        dom = open_browser_dom()
        domains = ['https://MarkSeaman.org', 'https://shrinking-world.com', 'https://SeamansLog.com',
                   'https://Spiritual-Things.org', 'http://unco-bacs.org/bacs200/class/templates/simple.html',
                   'http://unco-bacs.org']
        pages = []
        for url in domains:
            dom.get(url)
            pages = []
            default_features = ['head', 'head title', 'header h1', 'header h2', 'div.logo', 'nav',
                                'main h1', 'main h2', 'main p', 'main li', 'footer']
            pages.append(dom.page_source)
        close_browser_dom(dom)
        return '\n\n'.join(pages)

