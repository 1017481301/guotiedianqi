import time
from  Parts.Selector import *
from Dao import OraclePort
import re

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

# Tr_Td结构封装的表单，用于报警列表展示、缺陷确认、取消、定位修改等
class TrTdTable(object):
    def __init__(self,driver,locationID):
        self.driver=driver
        self.id=locationID  # 要求改页面下的列表

    def __mode(self):
        # 如果为多列标识一条信息返回True,单列返回False
        allTd=self.driver.find_element_by_id(self.id).find_element_by_tag_name('table').find_elements_by_tag_name('td')
        for td in allTd:
            if td.text!=None or td.text!='':
                return True
        return False

    def getInitValue(self):
        #判定tr-td封装模式
        initDatas=dict()
        elementValue=None
        elementID=None
        if self.__mode():  #真,代表多列模式
            allTr=self.driver.find_element_by_id(self.id).find_element_by_tag_name('table').find_elements_by_tag_name('tr')
            for tr in allTr:
                allTd=tr.find_elements_by_tag_name('td')
                for r in allTd:
                    elementTitle = (r.find_element_by_tag_name('label').text)[:-1]
                    # 首先完成当前控件类型判定
                    # elementHtml=r.find_element_by_tag_name('td').get_attribute('innerHTML')
                    for tag in ('input', 'textarea', 'select'):
                        try:
                            r.find_element_by_tag_name(tag)
                        except:
                            continue
                        else:
                            elementValue = r.find_element_by_tag_name(tag).get_attribute('value')

                            elementID=r.find_element_by_tag_name(tag).get_attribute('id')
                            time.sleep(1)
                            r.find_element_by_tag_name(tag).click()
                            childElements=self.driver.find_elements_by_css_selector('*[id*="'+elementID+'"')
                            minID=9999
                            childID=None

                            for cet in childElements:
                                cid = cet.get_attribute('id')
                                if cid != elementID:
                                    if len(cid) < minID:
                                        minID = len(cid)
                                        childID = cid
                            '''
                            if childID:
                                print(self.driver.find_element_by_css_selector('*[id*="' + childID + '"').text)
                                print(self.driver.find_element_by_css_selector('*[id*="' + childID + '"').get_attribute('id'))
                            '''
                    initDatas[elementTitle] = elementValue+'['+elementID+']'
        else:  # 假代表单列模式
            allTr=self.driver.find_element_by_id(self.id).find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')
            for tr in allTr:
                allTd=tr.find_elements_by_tag_name('td')
                for r in allTd:
                    elementTitle = (r.find_element_by_tag_name('label').text)[:-1]
                    # 首先完成当前控件类型判定
                    # elementHtml=r.find_element_by_tag_name('td').get_attribute('innerHTML')
                    for tag in ('input', 'textarea', 'select'):
                        try:
                            r.find_element_by_tag_name(tag)
                        except:
                            continue
                        else:
                            elementValue = r.find_element_by_tag_name(tag).get_attribute('value')

                            elementID=r.find_element_by_tag_name(tag).get_attribute('id')
                            time.sleep(1)
                            r.find_element_by_tag_name(tag).click()
                            childElements=self.driver.find_elements_by_css_selector('*[id*="'+elementID+'"')
                            minID=9999
                            childID=None

                            for cet in childElements:
                                cid = cet.get_attribute('id')
                                if cid != elementID:
                                    if len(cid) < minID:
                                        minID = len(cid)
                                        childID = cid
                            '''
                            if childID:
                                print(self.driver.find_element_by_css_selector('*[id*="' + childID + '"').text)
                                print(self.driver.find_element_by_css_selector('*[id*="' + childID + '"').get_attribute('id'))
                            '''
                    initDatas[elementTitle] = elementValue+'['+elementID+']'
        return initDatas

    def set(self,setValues):
        '''
        支持设置表单中的各个元素的值，默认为不选择
        :param setValues: 返回数据库中的一张表,包含元素名称、值等信息
        :return: 无返回值
        '''
        #initDatas = dict()
        #elementValue = None
        #elementID = None
        if self.__mode():  # 真,代表多列模式
            #获取表单行
            allTr = self.driver.find_element_by_id(self.id).find_element_by_tag_name('table').find_elements_by_tag_name('tr')
            for tr in allTr:
                #获取表单列，多列模式代表两个td是一套，前一个为title，后一个为元素操作值（通常为控件）
                allTd = tr.find_elements_by_tag_name('td')
                for r in allTd:
                    elementTitle = (r.find_element_by_tag_name('label').text)[:-1]
                    # 首先完成当前控件类型判定
                    # elementHtml=r.find_element_by_tag_name('td').get_attribute('innerHTML')
                    for tag in ('input', 'textarea', 'select'):
                        try:
                            r.find_element_by_tag_name(tag)
                        except:
                            continue
                        else:
                            elementID = r.find_element_by_tag_name(tag).get_attribute('id')
                            r.find_element_by_tag_name(tag).click()
                            listID=relateID(self.driver,elementID)
                            if listID!=None:
                                #获取属性用于判断当前控件调用什么控件方法
                                '''
                                elementClass=self.driver.find_element_by_id(listID).get_attribute('class')
                                if elementClass in self.componentRelate.keys():
                                    #如果这个class属性与其中的匹配，则调用componentRelate中的元素
                                    pass
                                    self.componentRelate.values()
                                '''
                                #Function代表调用名称(通过if-else实现)
                                Function=None
                                text="Hello"
                                if Function=='DivASelector':
                                    DivASelector(self.driver,listID).option("Hello")
                                elif Function=='UlLiSelector':
                                    UlLiSelector(self.driver,listID).option(1)
                                #通过反射机制实现将字符串转 Z换成类对象
                                class_fun=OraclePort.getFun("dtctest/dtctest@192.168.1.100/testdb")
                                if listID==None:

                                    elementClass=self.driver.find_element_by_id(listID).get_attribute('class')
                                    for fun_name,eclass,type in class_fun:
                                        if elementClass!='' and elementClass!=None:
                                            if elementClass==eclass:
                                                exec(fun_name+'(self.driver,)')
                                            else:
                                                continue
                                        else:



                                            if self.driver.find_element_by_tag_name(type):
                                                exec()
                                fun=Function+'('+self.driver+','+listID+').option('+text+')'
                                exec(fun)

                            else:
                                self.driver.find_element_by_id(elementID).get_attribute('class')
                                #或者直接进行操作
                                #self.driver.find_element_by_id(elementID).send_keys(setValues['text'])
                            '''
                            if childID:
                                print(self.driver.find_element_by_css_selector('*[id*="' + childID + '"').text)
                                print(self.driver.find_element_by_css_selector('*[id*="' + childID + '"').get_attribute('id'))
                            '''
                    #initDatas[elementTitle] = elementValue + '[' + elementID + ']'
        else:  # 假代表单列模式
            allTr = self.driver.find_element_by_id(self.id).find_element_by_tag_name('tbody').find_elements_by_tag_name(
                'tr')
            for tr in allTr:
                allTd = tr.find_elements_by_tag_name('td')
                for r in allTd:
                    elementTitle = (r.find_element_by_tag_name('label').text)[:-1]
                    # 首先完成当前控件类型判定
                    # elementHtml=r.find_element_by_tag_name('td').get_attribute('innerHTML')
                    for tag in ('input', 'textarea', 'select'):
                        try:
                            r.find_element_by_tag_name(tag)
                        except:
                            continue
                        else:
                            elementValue = r.find_element_by_tag_name(tag).get_attribute('value')

                            elementID = r.find_element_by_tag_name(tag).get_attribute('id')
                            time.sleep(1)
                            r.find_element_by_tag_name(tag).click()
                            childElements = self.driver.find_elements_by_css_selector('*[id*="' + elementID + '"')
                            minID = 9999
                            childID = None

                            for cet in childElements:
                                cid = cet.get_attribute('id')
                                if cid != elementID:
                                    if len(cid) < minID:
                                        minID = len(cid)
                                        childID = cid
                            '''
                            if childID:
                                print(self.driver.find_element_by_css_selector('*[id*="' + childID + '"').text)
                                print(self.driver.find_element_by_css_selector('*[id*="' + childID + '"').get_attribute('id'))
                            '''
                    #initDatas[elementTitle] = elementValue + '[' + elementID + ']'
        #return initDatas

class trtd_to_standard(object):
    def __init__(self,driver):
        '''
        初始化
        :param driver: 必须保证是最近上一层级
        '''
        self.driver=driver
        #self.id=locationID
    def to_standard(self):
        '''
        将非标准格式的表单转换成统一标准格式的表单:key,value
        :return :(key,value,attributes)
        '''
        tableMessage=dict()
        tableName='报警确认'
        print("首先得输出当前表的名称（唯一标记）：",tableName)

        rows = self.driver.find_elements_by_tag_name('tr')
        for r,n in rows,range(len(rows)):
            print('输出行号：',n)
            cols=r.find_elements_by_tag_name('td')
            for c in cols:
                tableMessage['tableName']=tableName  #手工填写，也可以通过特定信息获取
                tableMessage['rowNumber']=n          #自动获取
                tableMessage['tableKey']=''          #人工填写，可自动获取（检查表并获取表的定位方法）
                tableMessage['tableValue']=''        #人工填写，可自动获取方法相关的属性属性
                tableMessage['elementTitle']=''      #自动获取
                tableMessage['elementKey'] = ''      #人工填写，可自动获取（通过获取表格的属性）
                tableMessage['elementValue'] = ''    #人工填写，可自动获取方法相关的属性属性
                tableMessage['elementFunction'] = '' #人工关联操作方法，也可以通过特征匹配
                print('获取文本值',c.text)


