# _*_ coding=utf-8 _*_

import time

class LoginPage():

    def __init__(self,driver,url=None):
        print(driver)
        '''
        完成页面的打开和初始化操作
        初始化不传入地址，则通过其他方式获取页面初始化地址
        '''
        if url is None:
            pass
        else:
            driver.get(url)
            time.sleep(5)
        self.driver=driver

    #基础操作
    def usernameElement(self,username=None):
        '''操作用户名'''
        if username is None:
            #通过其他方式获取用户名
            pass
        else:
            deal=self.driver.find_element_by_id("username")
            deal.clear()
            deal.send_keys(username)

    def passwordElement(self,password=None):
        '''操作密码'''
        if password is None:
            pass
        else:
            deal=self.driver.find_element_by_id("password")
            deal.clear()
            deal.send_keys(password)

    def  rememberPassword(self):
        self.driver.find_element_by_id("rem_Password").click()

    def verificationCode(self,ver=None):
        '''南昌局专用安全验证'''
        if ver is None:
            pass
        deal=self.driver.find_element_by_id("VerificationCode")
        deal.clear()
        deal.send_keys(ver)

    def submit(self):
        "提交登录表单"
        deal=self.driver.find_element_by_class_name("login_go")
        deal.click()

    def closMessage(self):
        "关闭消息框"
        deal=self.driver.find_element_by_class_name("layui-layer-btn0")
        deal.click()

    #流程操作
    def login(self,username,password):
        self.usernameElement(username)
        self.passwordElement(password)
        self.submit()
    #文本或者提示获取
    def getHint(self):
        #hintMsg=self.driver.find_element_by_class_name("layui-layer-content_layui-layer-padding")
        time.sleep(1)
        return self.driver.find_element_by_xpath('//*[@id="layui-layer1"]/div[2]').text

    def getCopyRight(self):
        return self.driver.find_element_by_xpath('//*[@id="foot"]/p[1]').text

    def getSysMessage(self):
        return self.driver.find_element_by_xpath('//*[@id="foot"]/p[2]').text

    def userMessage(self):
        return self.driver.find_element_by_xpath('/html/body/div[2]/div[1]/label').text

    def getTitle(self):
        return self.driver.title

if __name__=='__main__':
    from selenium import webdriver
    driver=webdriver.Chrome()
    driver.get("http://183.203.132.154:9100")
    test=LoginPage(driver)
    #test.getHint()
    print(test.getCopyRight())
    print(test.getSysMessage())
    print(test.getTitle())
    print(test.userMessage())