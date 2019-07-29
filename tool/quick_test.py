from tool.page import end_browser, start_browser, page_features
# from tool.page import test_selenium_setup


def quick_test():
    # test_selenium_setup()
    driver = start_browser()
    url = 'https://Spiritual-Things.org'
    # driver.get(url)
    # print(driver.page_source)
    print(page_features(driver, url))
    end_browser(driver)
