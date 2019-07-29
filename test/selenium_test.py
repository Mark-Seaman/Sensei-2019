from tool.page import end_browser, start_browser, page_features


def selenium_features_test():
    driver = start_browser()
    features = []
    domains = ['https://MarkSeaman.org', 'https://shrinking-world.com', 'https://SeamansLog.com',
               'https://Spiritual-Things.org', 'http://unco-bacs.org/bacs200/class/templates/simple.html']
    for domain in domains:
        features.append(page_features(driver, domain))
    end_browser(driver)
    return '\n\n'.join(features)


if __name__ == '__main__':
    print(selenium_features_test())