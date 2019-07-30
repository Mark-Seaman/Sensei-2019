from tool.page import end_browser, start_browser, capture_page, extract_features, report_features


def quick_test():
    dom = start_browser()
    url = 'https://MarkSeaman.org'
    features = ['head', 'head title', 'header h1', 'header h2', 'div.logo', 'nav',
                'main h1', 'main h1', 'main p', 'main li', 'footer']
    capture_page(dom, url)
    # print(dom.page_source)
    features = extract_features(dom, features)
    print(report_features(url, features))
    end_browser(dom)
