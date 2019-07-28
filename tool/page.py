from os import system
from platform import node
from selenium import webdriver


def start_browser():
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    if node() == 'sensei-server':
        print('open display')
        from pyvirtualdisplay import Display
        display = Display(visible=0, size=(800, 600))
        display.start()
    else:
        options.add_argument('window-size=800x600')
        options.add_argument('headless')
    return webdriver.Chrome(options=options)


def end_browser(browser):
    browser.quit()


def find_css_selector(browser, selector):
    try:
        tag = browser.find_element_by_css_selector(selector)
        return tag.get_attribute("innerHTML")
    except:
        return '** No feature found: selector = %s **' % selector


def extract_features(browser, features):
    results = {}
    for t in features:
        results[t] = find_css_selector(browser, t)
    return results


def report_features(url, features):
    def feature_string(features, f):
        return '\n\n## %s\n\n %s' % (f, features[f])

    report = ['# Page Features for %s' % url]
    report += [feature_string(features, f) for f in features.keys()]
    return '\n'.join(report)


def get_requirements(url):
    if url == 'http://localhost:8000/MarkSeaman':
        return ['header h1', 'header h2', 'main h2#inventor', 'footer', 'p', 'nav', 'h1', 'h2', 'ul>li']
    else:
        return ['header', 'footer', 'p', 'h1', 'h2']


def verify_page(url='http://localhost:8000'):
    browser = start_browser()
    browser.get(url)
    features = extract_features(browser, get_requirements(url))
    report = report_features(url, features)
    end_browser(browser)
    return report


def test_selenium_setup():

    # Check the version of Chromedriver
    system('chromedriver --version')

    # Open the webdriver
    print("open browser")
    driver = start_browser()
    print('Web browser open')

    # Get a page
    print('get page')
    driver.get('http://shrinking-world.com')
    print('title = ' + driver.title)

    # Close the webdriver
    driver.quit()
    print('Web browser closed')

# def find_xpath(browser, xpath):
#     try:
#         tag = browser.find_element_by_xpath(xpath)
#         return tag.get_attribute("innerHTML")
#     except:
#         return '** No feature found: xpath = %s **' % xpath


# def find_tags(browser, tag):
#     tags = browser.find_elements_by_tag_name(tag)
#     label = "\n%s:\n" % tag
#     tags = [label + t.get_attribute("innerHTML") for t in tags]
#     return '\n'.join(tags)

# def find_xpaths(browser, xpath):
#     tags = browser.find_elements_by_xpath(xpath)
#     label = "\n%s:\n" % xpath
#     tags = [label + t.get_attribute("innerHTML") for t in tags]
#     return '\n'.join(tags)
#
#
# def selenium_startup_test():
#     if not is_server():
#         browser = start_browser()
#         browser.get('http://localhost:8000')
#         title = browser.title
#         end_browser(browser)
#         return title
#     else:
#         return 'Test is disabled on the Sensei-Server'
#
#
# def selenium_content_test():
#     if not is_server():
#         browser = start_browser()
#         browser.get('http://localhost:8000')
#         source = redact_css(browser.page_source)
#         end_browser(browser)
#         return source
#     else:
#         return 'Test is disabled on the Sensei-Server'
#