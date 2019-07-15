from selenium import webdriver


options = webdriver.ChromeOptions()
options.add_argument('window-size=800x841')
options.add_argument('headless')
browser = webdriver.Chrome(options=options)
browser.get('https://shrinking-world.com')
print(browser.title)

