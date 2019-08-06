from os import system
from pprint import PrettyPrinter

from tool.shell import banner, is_server, redact_css, text_join

display = ''


def capture_page(driver, url):
    try:
        driver.get(url)
    except:
        print("**error: capture_page(%s)" % url)


def capture_page_features(url='http://localhost:8000', requirements=None):
    dom = open_browser_dom()
    dom.get(url)
    features = check_page_features(dom, requirements)
    source = dom.page_source
    close_browser_dom(dom)
    return features, source


def capture_page_source(dom, url):
    capture_page(dom, url)
    return dom.page_source


def check_features(features):

    def check_feature(feature, actual, correct):
        if actual == correct:
            status = 'The requirement for %s is met.' % feature
        else:
            status = '** The requirement for %s is NOT met. Keep working. **' % feature
        return dict(status=status, feature=feature, actual=actual, correct=correct)

    results = []
    for f in features:
        results.append(check_feature(f['feature'], f['actual'], f['correct']))
    return results


def check_page_features(dom, requirements):
    features = extract_features(dom, requirements)
    return check_features(features)


def close_browser_dom(browser):
    browser.quit()
    if is_server():
        global display
        display.stop()


def extract_features(dom, features):
    results = []
    for t in features:
        f = redact_css(find_css_selector(dom, t))
        results.append(dict(feature=t, actual=f, correct='initial value'))
    return results


def find_css_selector(browser, selector):
    try:
        tag = browser.find_element_by_css_selector(selector)
        return tag.get_attribute("innerHTML")
    except:
        return '** No feature found: selector = %s **' % selector


def find_tags(browser, tag):
    tags = browser.find_elements_by_tag_name(tag)
    return [t.get_attribute("innerHTML") for t in tags]


def find_xpath(browser, xpath):
    try:
        tag = browser.find_element_by_xpath(xpath)
        return tag.get_attribute("innerHTML")
    except:
        return '** No feature found: xpath = %s **' % xpath


def find_xpaths(browser, xpath):
    tags = browser.find_elements_by_xpath(xpath)
    return [t.get_attribute("innerHTML") for t in tags]


def get_page_source(url):
    dom = open_browser_dom()
    capture_page(dom, url)
    print(redact_css(dom.page_source))
    close_browser_dom(dom)


def open_browser_dom():
    from selenium import webdriver
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    if is_server():
        from pyvirtualdisplay import Display
        global display
        display = Display(visible=0, size=(800, 600))
        display.start()
    else:
        options.add_argument('window-size=800x600')
        options.add_argument('headless')
    return webdriver.Chrome(options=options)


def requirements_summary(features):

    report = []
    for i,f in enumerate(features):
        report.append('\nRequirement #%s - %s:\n\n    %s' % (i+1, f['feature'], f['actual']))
    return text_join(report)


def report_requirements(features):
    return PrettyPrinter(indent=4, width=200).pformat(features)


def verify_page(dom, url, requirements):
    dom.get(url)
    features = check_page_features(dom, requirements)
    return banner(url) + '\n' + requirements_summary(features)


def test_selenium_setup():

    # Check the version of Chromedriver
    system('chromedriver --version')

    # Open the webdriver
    print("open browser")
    driver = open_browser_dom()
    print('Web browser open')

    # Get a page
    print('get page')
    driver.get('http://shrinking-world.com')
    print('Page Source:\n' + driver.page_source)

    # Close the webdriver
    driver.quit()
    print('Web browser closed')



