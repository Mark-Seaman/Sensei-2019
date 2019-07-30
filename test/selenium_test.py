from tool.page import close_browser_dom, open_browser_dom, capture_page, extract_features, report_features


def get_requirements(url):
    default_features = ['head', 'head title', 'header h1', 'header h2', 'div.logo', 'nav',
                        'main h1', 'main h1', 'main p', 'main li', 'footer']
    if url == 'https://MarkSeaman.org':
        return ['header h1', 'header h2', 'main h2#inventor', 'footer', 'p', 'nav', 'h1', 'h2', 'ul>li']
    elif url == 'http://unco-bacs.org/bacs200/class/templates/simple.html':
        return ['head', 'body', 'h1']
    else:
        return default_features


def selenium_features_test():
    dom = open_browser_dom()
    features = []
    domains = ['https://MarkSeaman.org', 'https://shrinking-world.com', 'https://SeamansLog.com',
               'https://Spiritual-Things.org', 'http://unco-bacs.org/bacs200/class/templates/simple.html']
    for url in domains:
        requirements = get_requirements(url)
        capture_page(dom, url)
        x = extract_features(dom, requirements)
        features.append(report_features(url, x))
    close_browser_dom(dom)
    return '\n\n'.join(features)


if __name__ == '__main__':
    print(selenium_features_test())