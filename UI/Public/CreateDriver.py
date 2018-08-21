import threading
from selenium import webdriver
class getBrowserDriver(object):
    _instance_lock = threading.Lock()

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if not hasattr(getBrowserDriver, "_instance"):
            with getBrowserDriver._instance_lock:
                if not hasattr(getBrowserDriver, "_instance"):
                    getBrowserDriver._instance = webdriver.Chrome()
                    #getBrowserDriver._instance = webdriver.PhantomJS()
                    #getBrowserDriver._instance = webdriver.Ie()
                    #getBrowserDriver._instance = webdriver.Firefox()
                    print(getBrowserDriver._instance)
        return getBrowserDriver._instance