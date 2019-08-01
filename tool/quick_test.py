from tool.page import open_browser_dom, close_browser_dom, verify_page


def quick_test():
    page = open_browser_dom()

    url = 'http://unco-bacs.org'
    requirements = ['head', 'body', 'h1', 'title']
    print(verify_page(page, url, requirements))

    url = 'https://MarkSeaman.org'
    requirements = ['header h1', 'header h2', 'main h2#inventor', 'footer', 'p', 'nav', 'h1', 'h2', 'ul>li']
    print(verify_page(page, url, requirements))

    ['header h1', 'header h2', 'main h2#inventor', 'footer', 'p', 'nav', 'h1', 'h2', 'ul>li']
    # url = 'https://MarkSeaman.org'
    # print(get_page_source(url))

    close_browser_dom(page)
