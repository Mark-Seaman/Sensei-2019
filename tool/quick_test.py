from tool.page import end_browser, start_browser, page_features
# from tool.page import test_selenium_setup


def quick_test():
    # test_selenium_setup()
    driver = start_browser()
    driver.get('http://localhost:8000/homework/unc/bacs200/Homework')
    print(driver.page_source)
    # print(page_features(driver, 'http://unco-bacs.org/bacs200/class/templates/simple.html',
    #                     ['head', 'head title', 'body h1', 'p']))
    end_browser(driver)
