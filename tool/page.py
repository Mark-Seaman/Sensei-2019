from os import system

from tool.shell import is_server
from tool.text import text_join, text_lines

display = ''


def capture_page(dom, url):
    try:
        dom.get(url)
        return dom.page_source
    except:
        print("**error: capture_page(%s)" % url)


def capture_page_features(dom, url, requirements):
    source = capture_page(dom, url)
    for r in requirements:
        r.actual = find_css_selector(dom, r.selector)
        if r.transform:
            r.actual = eval(r.transform)
        r.save()
    return source, requirements


def close_browser_dom(browser):
    browser.quit()
    if is_server():
        global display
        display.stop()


def count_chars(text, min, max):
    x = len(text)
    if x > max or x < min:
        return '%d Characters in output (should be between %s and %s)' % (len(text), min, max)
    else:
        return 'Characters in output (is between %s and %s)' % (min, max)


def count_lines(text, min, max):
    x = len(text_lines(text))
    if x > max or x < min:
        return '%d Lines in output (should be between %s and %s)' % (x, min, max)
    else:
        return 'Lines in output (is between %s and %s)' % (min, max)


def display_requirements(project):
    results = []
    for i, r in enumerate(project.requirements):
        results.append('\nRequirement #%s: %s   \n' % (r.num, r.selector))
        results.append('    Correct Output:     \n        %s' % r.correct)
        results.append('    Actual Output:      \n        %s' % r.actual)
        results.append('    Transform Output:   \n        %s' % r.transform)
        results.append('    Test Status:        \n        %s' % r.results)
    return text_join(results)


def display_test_results(data):
    results = []
    results.append('Student: %s' % data['student'])
    results.append('URL: %s' % data['url'])
    for i, r in enumerate(data['requirements']):
        # r.num = i + 1
        # r.save()
        results.append('Requirement: %s, %s, %s' % (r.num, r.selector, r.actual))
    return text_join(results)


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
