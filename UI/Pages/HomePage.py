# _*_ coding=utf-8 _*_
import time

class HomePage():
    def __init__(self,driver,url=None):
        '''
            完成页面的打开和初始化操作
            初始化不传入地址，则通过其他方式获取页面初始化地址
            '''
        if url is None:
            pass
            # BasePage.__init__(self, driver)
            # self.open(login_locators.get("login.url"))
        else:
            driver.get(url)
            time.sleep(5)
        self.driver = driver
    #页面操作
    def  pageDeal(self):
        pass

    def onLineMonitoring(self):
        '''在线实时检测'''
        self.driver.find_element_by_xpath('//*[@id="LeftTop"]/div[1]/a').click()

    def alarmMonitoring(self):
        '''报警监控'''
        self.driver.find_element_by_xpath('//*[@id="LeftTop"]/div[2]/a').click()

    def locomotiveMonitoring(self):
        '''车顶实时监控'''
        self.driver.find_element_by_xpath('//*[@id="LeftTop"]/div[2]/div[1]/a').click()

    def faultLibrary(self):
        '''缺陷库'''
        self.driver.find_element_by_xpath('//*[@id="RightTop"]/div[1]/a[1]').click()

    def activeDetection(self):
        '''主动检测'''
        self.driver.find_element_by_xpath('//*[@id="RightTop"]/div[1]/a[2]').click()

    def detectData(self):
        '''检测数据'''
        self.driver.find_element_by_xpath('//*[@id="RightTop"]/div[2]/a[1]').click()

    def quitSystem(self):
        "退出系统"
        self.driver.find_element_by_id("btn_close").click()
    # 页面流程

    # 获取页面信息
    def getUserMessage(self):
        #历史版本获取方式(version<=5.2.0)
        #return self.driver.find_element_by_id("UName").text
        #新版本获取方式(version>=5.2.0)
        return self.driver.find_element_by_id("Iname").text