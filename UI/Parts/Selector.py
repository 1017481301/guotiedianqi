# _*_ coding=utf-8 _*_
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select

'''
<说明：>:
封装下拉控件的操作封装，包含：
    -获取HTML结构
    -获取当前选择值(含初始值)
    -获取列表数据
    -操作
    -操作日志
    -其他信息
'''
#封装一个公共函数，完成控件内部关联
def relateID(driver,componentID):
    childElements = driver.find_elements_by_css_selector('*[id*="' + componentID + '"')
    minID = 9999
    childID = None
    for cet in childElements:
        cid = cet.get_attribute('id')
        if cid != componentID:
            if len(cid) < minID:
                minID = len(cid)
                childID = cid
    return childID

class DivASelector(object):#TextBoxWithList
    '''
    应用范围：
        3C：报警类型选择
    '''
    def __init__(self,driver,componentID):
        '''
        初始化类，参数说明如下：
        :param driver: 提供页面操作句柄，该句柄必须来自于webdriver
        :param componentID: 该控件关联文本框的ID（根据开发提供，所有控件必须操作ID）
        '''
        #判定driver的合法性，是否为webdriver
        if type(driver) is webdriver.chrome.webdriver.WebDriver:
            self.driver=driver
            self.componentID = str(componentID)
            self.selectElement=self.driver.find_element_by_id(self.componentID)#还需判定元素的存在性
        else:
            raise Exception("driver类型错误：非webdriver类型")
        #检测封装模式检查（暂时不做处理）

    #文本框支持直接输入
    def input(self,inputMes,mode='a'):
        '''
        直接输入文本信息，但是必须支持该页面才能调用
        :param inputMes: 输入内容
        :param mode: 输入模式a代表追加（默认），c代表清除原有内容
        :return: 返回输入后控件的value
        '''
        #判定mode是否合法
        if mode not in ('a','c'):
            raise Exception("模式(mode)选择错误，请输入'c'或者'a'")
        self.selectElement.click()  # 打开文件下拉
        if mode=='c':
            self.selectElement.clear()
        self.selectElement.send_keys(inputMes)
        return self.selectElement.get_attribute('value')

    def option(self,select,mode='text',order='last'):
        '''
        :param selectText:需要选择的文本
        :mode:模式分为序号选择number,文件选择text，带查询选择其中之一select(默认，不支持模糊匹配)
        :order:当mode='select'时，需要指定查询后哪个选项被选入,值分别为第一个first，最后一个last，任意一个anyone
        :return: 选择结果值
        '''
        #判定模式合法性
        if mode=='number':
            if type(select) is not int:
                try:
                    select=int(select)
                except:
                    raise Exception('select无法转换成数字，输入非法')
        elif mode in ('text','select'):
            select=str(select)
        else:
            raise Exception('mode模式非法，请选择"text"或者"number"')

        #操作部分
        self.driver.find_element_by_id(self.componentID).click()
        listID=relateID(self.driver,self.componentID)
        buttons = self.driver.find_element_by_id(listID).find_elements_by_tag_name('a')
        if mode=='text':
            for b in buttons:
                rText = b.text
                if select == rText:
                    b.click()
                    return self.selectElement.get_attribute('value')
        elif mode=='number':
            n=1
            for b in buttons:
                if n==select:
                    b.click()
                    return self.selectElement.get_attribute('value')
                n=n+1
        '''
        elif mode=='select':
            self.driver.find_element_by_id(self.componentID).send_keys(select)
            time.sleep(1)
            orows = self.driver.find_element_by_id(self.componentID).find_elements_by_tag_name('a')
            # 清除不显示的元素
            for r in orows:
                if r.is_displayed():
                    rows.append(r)
            # 选择其中之一
            if n <= len(rows) and n > 0:
                rows[n - 1].click()
                return n
            else:
                return -1
        
    def optionSelect(self,selectText,n=1):
        #当该控件支持模糊查询选项时可用
        rows = []
        self.driver.find_element_by_id(self.componentID).click()
        self.driver.find_element_by_id(self.componentID).send_keys(selectText)
        time.sleep(1)
        orows = self.driver.find_element_by_id(self.componentID).find_elements_by_tag_name('a')
        # 清除不显示的元素
        for r in orows:
            if r.is_displayed():
                rows.append(r)
        # 选择其中之一
        if n <= len(rows) and n > 0:
            rows[n - 1].click()
            return n
        else:
            return -1'''
    def clear(self):
        '''
        清除文本框中的所有信息
        :return:无返回值
        '''
        self.driver.find_element_by_id(self.componentID).clear()

    def getAllSelect(self):
        '''
        获取下拉中的所有选项
        :return: 按字典方式返回
        '''
        allSelect=dict()
        self.driver.find_element_by_id(self.componentID).click()
        listID = relateID(self.driver, self.componentID)
        groups=self.driver.find_elements_by_css_selector('#'+listID+' > div')
        for g in groups:
            title=g.find_elements_by_tag_name('/div[1]').find_element_by_tag_name('a').text
            allSelect[title]=[]
            lists=g.find_elements_by_tag_name('/div[1]').find_elements_by_tag_name('a')
            for  l in lists:
                allSelect[title].append(l.text)
        return allSelect


    def getInitValue(self):
        '''
        主要用于获取页面加载初始状态下的文本框值，也可以返回任意时刻的文本框值
        :return: 文本框当前值
        '''
        return self.driver.find_element_by_id(self.componentID).get_attribute('value')

class UlLiSelector(object):
    '''
        应用范围：
            3C：报警分析、处理建议
        '''

    def __init__(self, driver, componentID):
        '''
        初始化类，参数说明如下：
        :param driver: 提供页面操作句柄，该句柄必须来自于webdriver
        :param componentID: 该控件关联文本框的ID（根据开发提供，所有控件必须操作ID）
        '''
        # 判定driver的合法性，是否为webdriver
        if type(driver) is webdriver.chrome.webdriver.WebDriver:
            self.driver = driver
            self.componentID = str(componentID)
            self.selectElement = self.driver.find_element_by_id(self.componentID)  # 还需判定元素的存在性
        else:
            raise Exception("driver类型错误：非webdriver类型")
            # 检测封装模式检查（暂时不做处理）

    def input(self, inputMes, mode='a'):
        '''
        直接输入文本信息，但是必须支持该页面才能调用
        :param inputMes: 输入内容
        :param mode: 输入模式a代表追加（默认），c代表清除原有内容
        :return: 返回输入后控件的value
        '''
        # 判定mode是否合法
        if mode not in ('a', 'c'):
            raise Exception("模式(mode)选择错误，请输入'c'或者'a'")
        self.selectElement.click()  # 打开文件下拉
        if mode == 'c':
            self.selectElement.clear()
        self.selectElement.send_keys(inputMes)
        return self.selectElement.get_attribute('value')
    '''
    def select(self,selectMes,n=1):
        rows = []
        self.driver.find_element_by_id(self.componentID).click()
        self.driver.find_element_by_xpath('//*[@id="' + self.listID + '"]/preceding-sibling::div[1]/input').send_keys(selectMes)
        time.sleep(1)
        orows = self.driver.find_element_by_id(self.listID).find_elements_by_css_selector('li')
        # 清除不显示的元素
        for r in orows:
            if r.is_displayed():
                rows.append(r)
        # 选择其中之一
        if n <= len(rows) and n > 0:
            rows[n - 1].find_element_by_tag_name('a').click()
            return n
        else:
            return -1
    '''
    def option(self, select, mode='text', order='last'):
        '''
        :param selectText:需要选择的文本
        :mode:模式分为序号选择number,文件选择text，带查询选择其中之一select(默认，不支持模糊匹配)
        :order:当mode='select'时，需要指定查询后哪个选项被选入,值分别为第一个first，最后一个last，任意一个anyone
        :return: 选择结果值
        '''
        # 判定模式合法性
        if mode == 'number':
            if type(select) is not int:
                try:
                    select = int(select)
                except:
                    raise Exception('select无法转换成数字，输入非法')
        elif mode in ('text', 'select'):
            select = str(select)
        else:
            raise Exception('mode模式非法，请选择"text"或者"number"')

        # 操作部分
        self.driver.find_element_by_id(self.componentID).click()
        listID = relateID(self.driver, self.componentID)
        buttons = self.driver.find_element_by_id(listID).find_elements_by_tag_name('a')
        if mode == 'text':
            for b in buttons:
                rText = b.text
                if select == rText:
                    b.click()
        elif mode == 'number':
            n = 1
            for b in buttons:
                if n == select:
                    b.click()
                n = n + 1
        return self.selectElement.get_attribute('value')
    '''
    def optionWithText(self,selectText):
        self.driver.find_element_by_id(self.componentID).click()
        rows = self.driver.find_element_by_id(self.listID).find_elements_by_css_selector('li')
        for r in rows:
            rText = r.find_element_by_tag_name('a').text
            if selectText == rText:
                r.find_element_by_tag_name('a').click()
    def optionWithOrder(self,n):
        self.driver.find_element_by_id(self.componentID).click()
        rows = self.driver.find_element_by_id(self.listID).find_elements_by_css_selector('li')
        if n <= len(rows) and n > 0:
            rows[n - 1].find_element_by_tag_name('a').click()
            return n
        else:
            return -1
    '''
    def CheckOption(self,selectList,mode='text', order='last'):
        self.driver.find_element_by_id(self.componentID).click()
        listID = relateID(self.driver, self.componentID)
        liElements=self.driver.find_element_by_id(listID).find_elements_by_tag_name('li')
        for li in liElements:
            #li.find_element_by_tag_name('a')
            if mode == 'text':
                #for b in buttons:
                rText = li.find_element_by_tag_name('a').text
                if  rText in selectList:
                    li.find_element_by_css_selector('span[class*="button chk checkbox"]').click()
                    #return self.selectElement.get_attribute('value')
            elif mode == 'number':
                n = 1
                if n in selectList:
                    li.find_element_by_css_selector('span[class*="button chk checkbox"]').click()
                n = n + 1
        return self.selectElement.get_attribute('value').split(',')
    def getInitValue(self):
        '''
        主要用于获取页面加载初始状态下的文本框值，也可以返回任意时刻的文本框值
        :return: 文本框当前值
        '''
        return self.selectElement.get_attribute('value')

    def clear(self):
        '''
        清除文本框中的所有信息
        :return:无返回值
        '''
        self.selectElement.clear()
    def clearSelector(self):
        '''
        前置条件，进入了查询区域或者输入了查询信息
        :return: 返回True代表清除成功,False代表清除失败
        '''
        listID = relateID(self.driver, self.componentID)
        try:
            self.driver.find_element_by_xpath('//*[@id="' + listID + '"]/preceding-sibling::div[1]/a').click()
            return True
        except:
            return False

    def isReadOnly(self):
        '''
        判定是否文本框为只读模式
        :return: True代表返回只读，False代表非只读
        '''
        rd=self.selectElement.get_attribute('readonly')
        if rd=="readonly" or rd or rd==None:
            return True
        else:
            return False

class OptionSelector(Select):
    '''
    该类继承自官方给定的Select类
    应用范围：
        3C：报警级别
    '''
    def __init__(self,driver,componentID):
        '''
                初始化类，参数说明如下：
                :param driver: 提供页面操作句柄，该句柄必须来自于webdriver
                :param componentID: 该控件关联文本框的ID（根据开发提供，所有控件必须操作ID）
                '''
        # 判定driver的合法性，是否为webdriver
        if type(driver) is webdriver.chrome.webdriver.WebDriver:
            self.driver = driver
            self.componentID = str(componentID)
            self.selectElement = self.driver.find_element_by_id(self.componentID)  # 还需判定元素的存在性
        else:
            raise Exception("driver类型错误：非webdriver类型")
        #webelement=driver.find_element_by_id(componentID)
        Select.__init__(self.selectElement)
    def getInitValue(self):
        return self.selectElement.get_attribute('value')
     #等待是否封装

class AlarmCurveSelector(object):
    def __init__(self,driver,componentID):
        self.driver=driver
        self.componentID=componentID

    def option(self,select, mode='text', order='last'):
        self.driver.find_element_by_id(self.componentID).click()
        buttons = self.driver.find_element_by_id(self.componentID).find_elements_by_tag_name('a')
        if mode=='text':
            for b in buttons:
                rText = b.text
                if select == rText:
                    b.click()
        elif mode == 'number':
            n = 1
            for b in buttons:
                if n == select:
                    b.click()
                n = n + 1
    def getInitValue(self,componentID):
        return self.driver.find_element_by_id(componentID).find_element_by_id('chartTitle').text

if __name__=="__main__":
    url1='http://222.33.59.186:10001'
    url='http://222.33.59.186:10001/C3/PC/MAlarmMonitoring/MonitorAlarm3CForm4.htm?alarmid=Fcfb95f366d9146658d3a16602ebfaa2c'
    #driver=CreateDriver.getBrowserDriver()
    driver=webdriver.Chrome()
    print(driver)
    driver.maximize_window()
    driver.get(url1)
    driver.find_element_by_id('username').send_keys('admin')
    driver.find_element_by_id('password').send_keys('cdgt@qwer')
    driver.find_element_by_class_name("login_go").click()
    driver.get(url)
    t=tempSelector(driver)
    print(t.getOptionMes('chartTitle'))