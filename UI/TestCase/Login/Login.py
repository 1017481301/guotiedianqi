# _*_ coding=utf-8 _*_
#import HtmlTestRunner
from Report import HTMLTestReportCN
import time
import unittest
from selenium import webdriver
from ddt import ddt,data,unpack
#自定义包
from Pages import LoginPage
from Pages import HomePage
from Dao import OraclePort
from Public import CreateDriver
from BusinessObject import C3

@ddt
class TestLogin(unittest.TestCase):
    def setUp(self):
        '''该函数主要完成每个测试用例的初始换工作'''

        url = "http://192.168.1.101:10020"

        self.driver=CreateDriver.getBrowserDriver()
        time.sleep(1)
        self.page=LoginPage.LoginPage(self.driver, url)
        self.homePage=HomePage.HomePage(self.driver)


    @unpack
    @data(*(OraclePort.getTestData("dtctest/dtctest@192.168.1.100/testdb"))) #通过*可以将变量值拆分成多个单个元素
    def t2est_login(self,username,password,flag,result):
        self.page.login(username, password)
        #C3.login(username,password)
        print(username,password,flag,result)
        time.sleep(3)
        if flag=='LOGIN_SUCCESS':
            self.assertEqual(self.homePage.getUserMessage(), result, msg="检查失败，预期值：["+result+"]实际结果：["+self.homePage.getUserMessage()+']')
        else:
            self.assertEqual(self.page.getHint(),result,msg="检查失败，预期值：["+result+"]实际结果：["+self.page.getHint()+']')

    def test_allRight(self):
        self.page.login(username, password)
        #C3.login('admin','cdgt@qwer')
        #断言判定
        self.assertEqual(self.homePage.getUserMessage(),"admin(超级管理员)",msg="登录失败，用户名不等于输入值，或者未获取到")

    def test_passwordError(self):
        self.page.login(username, password)
        #C3.login('admin', 'ErrorPassword')
        self.assertEqual(self.page.getHint(),'登录失败：密码错误！，还有7次机会',msg="登录提示不正确")

    def tearDown(self):
        time.sleep(1)
        '''判定是否登录，如果登录则退出，等待下次测试用例执行'''
        try:
            self.homePage.quitSystem()
        except:
            pass
        #self.driver.quit()

if __name__ == '__main__':
    #my_driver.maximize_window()
    unittest.main()
    #suite = unittest.TestLoader().loadTestsFromTestCase(TestLogin)
    #unittest.TextTestRunner(verbosity=2).run(suite)

    #suite=unittest.TestSuite()
    #suite.addTest(TestLogin("test_passwordError"))
    #suite.addTest(TestLogin("test_allRight"))
    #suite.addTest(TestLogin("test_mlogin",(1,2,3)))
    #suite.addTest(TestLogin("test_mylogin"))
    #suite = unittest.TestLoader().loadTestsFromTestCase(Test)
    #输出到平台
    #runner=unittest.TextTestRunner(verbosity=2)
    #输出到测试报告(Python原生)
    #runner=HtmlTestRunner.HTMLTestRunner(output='D:/TestResult',report_title="3C数据中心测试报告",descriptions=True,verbosity=3)
    #输出到测试报告(网上优化版本)
    #filePath ='D:/TestResult/LoginTest.html'
    #fp = open(filePath,'wb')
    #runner=HTMLTestReportCN.HTMLTestRunner(stream=fp,title='登录测试报告',description='3C数据中心登录测试演示...',tester="梁钟")
    #runner.run(suite)
    #fp.close()
    #my_driver.quit()
