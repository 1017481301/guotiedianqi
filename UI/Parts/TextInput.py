# _*_ coding=utf-8 _*_
import time
"""
class TextBoxWithSelector(object):
    '''
    封装说明：
        <textarea name="UtxtAdvice" id="UtxtAdvice" ...></textarea>
        <ul id="ULUtxtAdvice"...>
            <li id="ULUtxtAdvice_1"...>
                <span id="ULUtxtAdvice_1_switch" ...></span>
                <a id="ULUtxtAdvice_1_a"...title="停电车巡">
                    <span id="ULUtxtAdvice_1_ico" ...></span>
                    <span id="ULUtxtAdvice_1_span">停电车巡</span>
                </a>
            </li>
            <li id="ULUtxtAdvice_2" ...>
                <span id="ULUtxtAdvice_2_switch" ...></span>
                <a id="ULUtxtAdvice_2_a" ...title="天窗检修">
                    <span id="ULUtxtAdvice_2_ico"...></span>
                    <span id="ULUtxtAdvice_2_span">天窗检修</span>
                </a>
            </li>
        </ul>
    '''
    def __init__(self,driver,componentID,prefix='',postfix=''):
        self.listID = str(prefix) + str(componentID) + str(postfix)
        self.componentID=str(componentID)
        self.driver=driver
        '''检测封装模式是否满足条件'''

    def input(self,inputMes):
        self.driver.find_element_by_id(self.componentID).click()  # 打开文件下拉
        self.driver.find_element_by_id(self.componentID).send_keys(inputMes)
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
    def optionWithText(self,selectText):
        self.driver.find_element_by_id(self.componentID).click()
        rows = self.driver.find_element_by_id(self.listID).find_elements_by_css_selector('li')
        for r in rows:
            rText = r.find_element_by_xpath('./a[1]/span[2]').text
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
    def getInputMes(self):
        return self.driver.find_element_by_id(self.componentID).get_attribute('value')
    def clear(self):
        #清除文本框中的所有信息
        self.driver.find_element_by_id(self.componentID).clear()
    def clearSelector(self):
        #前置条件，进入了查询区域或者输入了查询信息
        try:
            self.driver.find_element_by_xpath('//*[@id="' + self.listID + '"]/preceding-sibling::div[1]/a').click()
            return True
        except:
            return False
    def isReadOnly(self):
        rd=self.driver.find_element_by_id(self.componentID).get_attribute('readonly')
        if rd=="readonly" or rd or rd==None:
            return True
        else:
            return False
"""
class CommonTexBox(object):
    def __init__(self,driver,componentID):
        self.componentID=str(componentID)
        self.driver=driver
        '''检测封装模式是否满足条件'''

    def input(self,inputMes,mode='c'):
        '''

        :param inputMes:
        :param mode:追加模式'a',清楚原有值重新输入,'c'
        :return:
        '''
        self.driver.find_element_by_id(self.componentID).clear()
        self.driver.find_element_by_id(self.componentID).send_keys(inputMes)
        return self.driver.find_element_by_id(self.componentID).get_attribute('value')

    def getInitValue(self):
        return self.driver.find_element_by_id(self.componentID).get_attribute('value')

    def clear(self):
        self.driver.find_element_by_id(self.componentID).clear()
"""
class TextBoxWithSelector_2(object):
    def __init__(self,driver,componentID,prefix='',postfix=''):
        self.listID = str(prefix) + str(componentID) + str(postfix)
        self.componentID=str(componentID)
        self.driver=driver
        '''检测封装模式是否满足条件'''

    def input(self,inputMes):
        self.driver.find_element_by_id(self.componentID).click()  # 打开文件下拉
        self.driver.find_element_by_id(self.componentID).send_keys(inputMes)
    def select(self,selectMes,n=1):
        rows = []
        self.driver.find_element_by_id(self.componentID).click()
        self.driver.find_element_by_xpath('//*[@id="' + self.listID + '"]/div[1]/input').send_keys(selectMes)
        time.sleep(1)
        orows = self.driver.find_element_by_xpath('//*[@id="' + self.listID + '"]/div[2]').find_elements_by_tag_name('span')
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
    def optionWithText(self,selectText):
        self.driver.find_element_by_id(self.componentID).click()
        rows = self.driver.find_element_by_xpath('//*[@id="' + self.listID + '"]/div[2]').find_elements_by_tag_name('span')
        for r in rows:
            rText = r.text
            if selectText == rText:
                r.click()
    def optionWithOrder(self,n):
        self.driver.find_element_by_id(self.componentID).click()
        rows = self.driver.find_element_by_xpath('//*[@id="' + self.listID + '"]/div[2]').find_elements_by_tag_name('span')
        if n <= len(rows) and n > 0:
            rows[n - 1].click()
            return n
        else:
            return -1
    def getInputMes(self):
        return self.driver.find_element_by_id(self.componentID).get_attribute('value')
    def clear(self):
        #清除文本框中的所有信息
        self.driver.find_element_by_id(self.componentID).clear()
    def clearSelector(self):
        #前置条件，进入了查询区域或者输入了查询信息
        try:
            self.driver.find_element_by_xpath('//*[@id="' + self.listID + '"]/div[1]/a').click()
            return True
        except:
            return False
        pass
"""
class measureStagger(object):
    def __init__(self,driver,componentID):
        self.driver=driver
        self.id=componentID

    def measure(self):
        self.driver.find_element_by_id('btn_Set_jc').click()




if __name__=='__main__':
    pass
