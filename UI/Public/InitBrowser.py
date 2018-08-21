# _*_ coding=utf-8 _*_

'''
功能介绍：
    本功能模块主要完成浏览器的调用、初始化、关闭等操作
其他说明：
    ...
'''

from functools import wraps
'''
def singleton(cls):
    instances = {}
    @wraps(cls)
    def getinstance(*args, **kw):
        if cls not in instances:
            instances[cls]=MyDriver()
            #instances[cls] = cls(*args, **kw)
        return instances[cls]
    return getinstance

@singleton
class MyDriver(object):
    def __init__(self):
        print(webdriver.Chrome())
'''
my_driver=None
from selenium import webdriver
class UseBrowser(object):
    #self.driver=''
    def setupChrome(self,url=None):
        #global  my_driver
        my_driver=webdriver.Chrome()
        #self.driver.get(url)
        #self.driver.maximize_window()
        #return my_driver
    def setupIE(self,url):
        self.driver = webdriver.Ie()
        self.driver.get(url)
        self.driver.maximize_window()
        return self.driver
    def setupFirefox(self,url):
        self.driver = webdriver.Firefox()
        self.driver.get(url)
        self.driver.maximize_window()
        return self.driver
    def teardownBrowser(self):
        self.driver.close()
if __name__=='__main__':
    MyDriver()
    MyDriver()
    MyDriver()
    #d=UseBrowser()
    #d.setupChrome('http://www.baidu.com')
    #print(my_driver)