from selenium import webdriver
from pyvirtualdisplay import Display

print('Selenium Test')

# options = webdriver.ChromeOptions()
# options.add_argument('--window-size=800x841')
# options.add_argument('--headless')
# options.add_argument('--no-sandbox')

display = Display(visible=0, size=(800,600))
display.start()
print('Display Created')

print('Create Webdriver')
browser = webdriver.Chrome()
print('Get page')
browser.set_page_load_timeout(2)
browser.get('https://shrinking-world.com')
print(browser.page_source)

print('Close browser')
browser.quit()

print('Stop display')
display.stop()

