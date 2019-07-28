from selenium import webdriver
from os import system
from platform import node


def quick_test():

    # Check the version of Chromedriver
    system('chromedriver --version')

    # Setup options
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')

    # Add fake display for Ubuntu
    if node() == 'sensei-server':
        print('open display')
        from pyvirtualdisplay import Display
        display = Display(visible=0, size=(800, 600))
        display.start()
    else:
        options.add_argument('window-size=800x841')
        options.add_argument('headless')

    # Open the webdriver
    print("open browser")
    driver = webdriver.Chrome(chrome_options=options)
    print('Web browser open')

    # Get a page
    print('get page')
    driver.get('http://shrinking-world.com')
    print('title = ' + driver.title)

    # Close the webdriver
    driver.quit()
    print('Web browser closed')

