from tool.page import end_browser, start_browser, page_features


def selenium_features_test():
    driver = start_browser()
    features = page_features(driver, 'https://shrinking-world.com')
    features += page_features(driver, 'https://MarkSeaman.org')
    features += page_features(driver, 'https://SeamansLog.com')
    features += page_features(driver, 'https://Spiritual-Things.org')
    features += page_features(driver, 'http://unco-bacs.org/bacs200/class/templates/simple.html')
    end_browser(driver)
    return features


if __name__ == '__main__':
    print(selenium_features_test())