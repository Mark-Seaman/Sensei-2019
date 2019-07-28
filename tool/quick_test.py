from selenium import webdriver
from os import system
from pyvirtualdisplay import Display


def quick_test():

    system('chromedriver --version')
    print('open display')

    display = Display(visible=0, size=(800, 600))
    display.start()

    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')

    print("open browser")
    driver = webdriver.Chrome(chrome_options=options)
    driver.get('http://shrinking-world.com')
    print('title = ' + driver.title)


    driver.quit()
    print('Web browser open')

