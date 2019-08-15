from os import system
from os.path import join
from django.utils.timezone import now

from tool.shell import is_server, redact_css
from tool.text import text_join
from unc.models import Project

display = ''


def approve_requirements(project):
    for i, r in enumerate(project.requirements):
        r.correct = r.actual
        r.save()


def capture_page(dom, url):
    try:
        dom.get(url)
        return dom.page_source
    except:
        print("**error: capture_page(%s)" % url)


def capture_page_features(url, requirements):
    dom = open_browser_dom()
    source = capture_page(dom, url)
    check_page_features(dom, requirements)
    close_browser_dom(dom)
    return source


def check_page_features(dom, requirements):
    for r in requirements:
        r.actual = redact_css(find_css_selector(dom, r.selector))
        # r.actual = eval('count_chars(r.actual)')
        r.save()


def close_browser_dom(browser):
    browser.quit()
    if is_server():
        global display
        display.stop()


def count_chars(text):
    return '%d characters in output' % len(text)


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
        r.num = i + 1
        r.save()
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


def validate_project_page(course, project):
    p = Project.lookup(course, project)
    url = join('http://unco-bacs.org', p.page)
    source = capture_page_features(url, p.requirements)
    student = 'Mark Seaman'
    return dict(student=student, url=url, requirements=p.requirements, source=source, date=now())


def check_requirements(project):
    for i, r in enumerate(project.requirements):
        # if r.correct == 'Test not run yet':
        #     r.correct = r.actual
        if r.actual == r.correct:
            r.results = eval('count_chars(r.actual)')
        else:
            r.results = 'FAIL'
        r.save()


