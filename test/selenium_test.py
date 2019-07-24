from tool.shell import is_server, is_macbook
from tool.page import verify_page


def selenium_features_test():
    if not is_server() and not is_macbook():
        return verify_page('http://localhost:8000/MarkSeaman')
    else:
        return 'Test is disabled on the Sensei-Server'


if __name__ == '__main__':
    print(selenium_features_test())