from selenium import webdriver

def selenium_startup_test():

    options = webdriver.ChromeOptions()
    options.add_argument('window-size=800x841')
    options.add_argument('headless')
    browser = webdriver.Chrome(options=options)
    # browser.get('https://%s' % url)
    # browser = webdriver.Firefox()
    browser.get('http://localhost:8000')
    title = browser.title
    browser.quit()
    return title

