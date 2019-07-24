# from selenium import webdriver

from tool.management.commands.code import execute_command
# from tool.shell import is_server, redact_css
from tool.page import verify_page


def quick_test():
    print(verify_page())


# def start_browser():
#     options = webdriver.ChromeOptions()
#     options.add_argument('window-size=800x841')
#     options.add_argument('headless')
#     return webdriver.Chrome(options=options)
#
#
# def end_browser(browser):
#     browser.quit()
#
#
# def find_xpath(browser, xpath):
#     try:
#         tag = browser.find_element_by_xpath(xpath)
#         return tag.get_attribute("innerHTML")
#     except:
#         return '** No feature found: xpath = %s **' % xpath
#
#
# def extract_features(browser, features):
#     results = {}
#     for t in features:
#         results[t] = find_xpath(browser, '//' + t)
#     return results
#
#
# def report_features(features):
#     def feature_string(features, f):
#         return '\n\n## %s\n\n %s' % (f, features[f])
#
#     report = ['# Page Features for http://localhost:8000']
#     report += [feature_string(features, f) for f in features.keys()]
#     return '\n'.join(report)
#
#
# def page_features():
#     if not is_server():
#         browser = start_browser()
#         browser.get('http://localhost:8000')
#         features = extract_features(browser, ['header', 'main', 'foxoter', 'p', 'nav', 'h1', 'h2', 'ul/li'])
#         report = report_features(features)
#         end_browser(browser)
#         return report
#     else:
#         return 'Test is disabled on the Sensei-Server'
#
#
#
#
#

def search_test():
    execute_command('search doc info August')
    execute_command('search html h1 title')
    execute_command('search code info def')


