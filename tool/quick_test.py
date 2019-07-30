from tool.page import capture_page, close_browser_dom, extract_features, open_browser_dom, check_features


def quick_test():
    page_features_test()


def page_features_test():
    dom = open_browser_dom()
    url = 'https://MarkSeaman.org'
    features = ['head', 'head title', 'header h1', 'header h2', 'div.logo', 'nav',
                'main h1', 'main h1', 'main p', 'main li', 'footer']
    capture_page(dom, url)
    # print(dom.page_source)
    features = extract_features(dom, features)
    print(check_features(features, features))
    close_browser_dom(dom)


def page_source_test():
    dom = open_browser_dom()
    url = 'https://MarkSeaman.org'
    capture_page(dom, url)
    print(dom.page_source)
    close_browser_dom(dom)
