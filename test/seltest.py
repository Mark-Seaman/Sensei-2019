from selenium import webdriver
from pyvirtualdisplay import Display
from os import system


for loop in range(100):

    print('Selenium Test (loop %s)' % loop)
    display = Display(visible=0, size=(800,600))
    display.start()
    # print('Display Created')

    # print('Create Webdriver')
    browser = webdriver.Chrome()
    # print('Get page')
    browser.set_page_load_timeout(2)
    browser.get('https://shrinking-world.com')
    print('%s byte in page' % len(browser.page_source))

    # print('Close browser')
    browser.quit()

    # print('Stop display')
    display.stop()

    system('python manage.py system procs')

