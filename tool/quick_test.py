from tool.page import check_page_features, open_browser_dom, close_browser_dom, requirements_summary
from tool.shell import banner


def quick_test():
    page = open_browser_dom()

    url = 'http://unco-bacs.org'
    requirements = ['head', 'body', 'h1', 'title']

    url = 'https://MarkSeaman.org'
    requirements = ['header h1', 'header h2', 'main h2#inventor', 'footer', 'p', 'nav', 'h1', 'h2', 'ul>li']

    page.get(url)

    features = check_page_features(page, requirements)
    print(banner(url))
    print(requirements_summary(features))

    ['header h1', 'header h2', 'main h2#inventor', 'footer', 'p', 'nav', 'h1', 'h2', 'ul>li']
    # url = 'https://MarkSeaman.org'
    # print(get_page_source(url))

    close_browser_dom(page)
