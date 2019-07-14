from selenium import webdriver


def start_browser():
    options = webdriver.ChromeOptions()
    options.add_argument('window-size=800x841')
    options.add_argument('headless')
    return webdriver.Chrome(options=options)


def end_browser(browser):
    browser.quit()


def find_tags(browser, tag):
    tags = browser.find_elements_by_tag_name(tag)
    label = "\n%s:\n" % tag
    tags = [label + t.get_attribute("innerHTML") for t in tags]
    return '\n'.join(tags)


def find_xpath(browser, xpath):
    tags = browser.find_elements_by_xpath(xpath)
    label = "\n%s:\n" % xpath
    tags = [label + t.get_attribute("innerHTML") for t in tags]
    return '\n'.join(tags)


def selenium_startup_test():
    browser = start_browser()
    browser.get('http://localhost:8000')
    title = browser.title
    end_browser(browser)
    return title


def selenium_content_test():
    browser = start_browser()
    browser.get('http://localhost:8000')
    source = browser.page_source
    end_browser(browser)
    return source


def selenium_features_test():
    browser = start_browser()
    browser.get('http://localhost:8000')
    tags = ['header', 'main', 'footer', 'p', 'nav', 'h1', 'h2', 'ul/li']
    results = [find_xpath(browser, '//'+t) for t in tags]
    end_browser(browser)
    return '\n'.join(results)


if __name__ == '__main__':
    print(selenium_features_test())