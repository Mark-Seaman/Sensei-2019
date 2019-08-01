
from tool.page import close_browser_dom, open_browser_dom, verify_page
from tool.shell import is_server


def get_requirements(url):
    default_features = ['head', 'head title', 'header h1', 'header h2', 'div.logo', 'nav',
                        'main h1', 'main h1', 'main p', 'main li', 'footer']
    if url == 'https://MarkSeaman.org':
        return ['header h1', 'header h2', 'main h2#inventor', 'footer', 'p', 'nav', 'h1', 'h2', 'ul>li']
    elif url == 'http://unco-bacs.org/bacs200/class/templates/simple.html':
        return ['head', 'body', 'h1']
    elif url == 'http://unco-bacs.org':
        return ['head', 'body', 'h1']
    else:
        return default_features


def selenium_features_test():
    if is_server():
        return 'No Selenium on Sensei Server'
    else:
        dom = open_browser_dom()
        domains = ['https://MarkSeaman.org', 'https://shrinking-world.com', 'https://SeamansLog.com',
                   'https://Spiritual-Things.org', 'http://unco-bacs.org/bacs200/class/templates/simple.html',
                   'http://unco-bacs.org']
        pages = []
        for url in domains:
            requirements = get_requirements(url)
            pages.append(verify_page(dom, url, requirements))
        close_browser_dom(dom)
        return '\n\n'.join(pages)


if __name__ == '__main__':
    print(selenium_features_test())