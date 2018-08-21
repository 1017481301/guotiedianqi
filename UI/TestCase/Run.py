from Public import InitBrowser
import TestCase
if __name__ == '__main__':
    driver=InitBrowser.UseBrowser().setupChrome()
    TestCase.test_login.TestLogin()