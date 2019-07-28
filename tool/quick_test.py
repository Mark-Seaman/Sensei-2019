# from tool.management.commands.code import execute_command

from selenium import webdriver


def quick_test():
    options = webdriver.ChromeOptions()
    options.add_argument('window-size=800x841')
    options.add_argument('headless')
    browser = webdriver.Chrome(options=options)
    print('Web browser open')
    # print(verify_page())

# def search_test():
#     execute_command('search doc info August')
#     execute_command('search html h1 title')
#     execute_command('search code info def')
#

