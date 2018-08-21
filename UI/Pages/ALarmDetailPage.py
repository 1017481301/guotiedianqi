# _*_ coding=utf-8 _*_
import time
from Public import CreateDriver
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from Parts import TableBox

# 常量定义
# textBoxWithSelect函数的输入方式
TEXT_INPUT = 1
LIKE_INPUT = 2
CHOICE_INPUT = 3
#textBoxWithSelect 序号、文本、value
ORDER = 1
TEXT = 2





class AlarmDetail():
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
        self.driver = driver

    def confirm(self):
        '''报警确认'''
        self.driver.find_element_by_id('E_btnOk2').click()
    def cancel(self):
        '''报警取消'''
        self.driver.find_element_by_id('E_btnCan2').click()
    def replay(self):
        '''回放'''
        self.driver.find_element_by_id('btn_replay').click()
    def task(self):
        '''任务管理'''
        self.driver.find_element_by_id('E_btnTask').click()
    def preData(self):
        '''前一条数据'''
        self.driver.find_element_by_id('S_pre').click()
    def nextData(self):
        '''后一条数据'''
        self.driver.find_element_by_id('S_next').click()
    def closeAlarm(self):
        '''报警页关闭'''
        self.driver.find_element_by_id('S_btclose').click()
    def export(self):
        self.driver.find_element_by_xpath('//*[@id="btns_all"]/div[2]/a').click()
    def setAddr(self):
        self.driver.find_element_by_id('btn_editWZ').click()
    def sendMessage(self):
        self.driver.find_element_by_id('btn_sendinfo').click()
    def getCurve(self,):
        self.driver.find_element_by_id('divDropButton').click() #功能打开
        self.driver.find_element_by_id('').click()

    #other object

    def textBoxWithSelect(self,inputMes,inputMode,componentID,prefix='',postfix='',selectMode=TEXT,n=2,isReadOnly=True):
        '''
        函数封装了带查询和快捷方式输入的文本输入框的基本操作
        :param inputMes: 输入文本信息
        :param inputMode: 输入模式分为：
            TEXT_INPUT=1：文本框直接输入
            LIKE_INPUT=2：通过模式查询的方式选择下拉列表中的值进行快捷输入
            CHOICE_INPUT=3：直接选择下拉列表的值进行输入
        :param componentID: 控件定位主ID
        :param selectMode: 选择下拉列表方式分为：
            ORDER = 1：通过下拉列表的顺序定位选择
            TEXT = 2：通过下拉列表的展示内容定位选择
        :param prefix: 控件下拉列表定位前缀ID
        :param postfix: 控件下拉列表定位后缀ID
        :param isReadOnly: 默认READ_ONLY，可选READ_WRITE
        :return: 返回值None
        '''

        self.driver.find_element_by_id(componentID).click()   #打开文件下拉
        time.sleep(1)
        #self.driver.find_element_by_xpath('//*[@id="'+id+'"]/../div[1]/a').click()  #查询下拉清除
        if  inputMode==TEXT_INPUT:
            '''
            if isReadOnly:
                try:
                    if self.driver.find_element_by_id(componentID).get_attribute('readonly')=='readonly':
                        print('1不是只读模式')
                        return
                except:
                    print('不是只读模式')
                    return'''
            self.driver.find_element_by_id(componentID).send_keys(inputMes)
        elif inputMode==LIKE_INPUT:
            self.driver.find_element_by_xpath('//*[@id="'+str(prefix)+ componentID + str(postfix)+'"]/preceding-sibling::div[1]/input').send_keys(inputMes)
            #self.driver.find_element_by_xpath('//*[@id="'+str(prefix)+ componentID +'_'+str(n)+'_span"]').click()
            time.sleep(1)
            fix = self.driver.find_element_by_id(str(prefix) + componentID + str(postfix))
            orows=fix.find_elements_by_css_selector('li')
            rows=[]
            #清除不显示的元素
            for r in orows:
                if r.is_displayed():
                    rows.append(r)
            #选择其中之一
            if n <= len(rows) and n > 0:
                rows[n - 1].find_element_by_tag_name('a').click()
            else:
                return -1
        elif inputMode==CHOICE_INPUT:
            rows = self.driver.find_element_by_id(str(prefix) + componentID + str(postfix)).find_elements_by_css_selector('li')
            if selectMode==TEXT:
                for r in rows:
                    rText=r.find_element_by_xpath('./a[1]/span[2]').text
                    if inputMes == rText:
                        r.find_element_by_tag_name('a').click()
            elif selectMode==ORDER:
                if n<=len(rows) and n>0:
                    rows[n-1].find_element_by_tag_name('a').click()
                else:
                    return -1
            else:
                return -1   #输入值错误


    def serverity(self,choice,serID):
        #serID='Useverity'
        #self.driver.switch_to_frame('iframe_AlarmSure')  # 非封装区域
        Select(self.driver.find_element_by_id(serID)).select_by_visible_text(choice) #官方提供的方式
        '''
        #自己实现的方式
        self.driver.find_element_by_id(serID).click()
        serTags=self.driver.find_element_by_id('Useverity').find_elements_by_tag_name('option')
        for s in serTags:
            print(s.text)
            if s.text==choice:
                s.
                #s.click()
                #ActionChains(self.driver).move_to_element(s).click(s).perform()
                break
        '''
    def codeMenuTree(self,choice,subID, prefix='',postfix=''):
        #buttonID='citySel'
        self.driver.find_element_by_id(subID).click()
        alarmCodes=self.driver.find_element_by_id(prefix+subID+postfix).find_elements_by_tag_name('a')
        for code in alarmCodes:
            if code.text==choice:
                code.click()
                break

    def getAlarmMes(self):
        '''

        :return:
        '''
        alarmDatas=dict()

        for i in range(3):
            title = ''
            point='//*[@id="TOP_three"]/div['+str(i+1)+']'
            localElements=self.driver.find_element_by_xpath(point+'/div[1]/span[2]').find_elements_by_tag_name('span')
            for l in localElements:
                title+=l.text
            alarmDatas[title]=dict()
            localDataElements=self.driver.find_element_by_xpath(point+'/div[2]/ul').find_elements_by_tag_name('li')
            #print(localDataElements)
            for ld in localDataElements:
                key=ld.find_element_by_xpath('./label/span[1]').text
                value=ld.find_element_by_xpath('./span[1]').text
                alarmDatas[title][key]=value
        print(alarmDatas)
    def playControl(self,control_mode='ALL'):
        '''

        :param control_mode:
        :return:
        '''
        #控制条件判定
        if control_mode=='ALL':
            self.driver.find_element_by_xpath('//*[@id="note"]/a[1]').click()
            self.driver.find_element_by_xpath('//*[@id="note"]/a[2]').click()
            self.driver.find_element_by_xpath('//*[@id="note"]/a[3]').click()
            self.driver.find_element_by_xpath('//*[@id="note"]/a[4]').click()
            self.driver.find_element_by_xpath('//*[@id="note"]/a[5]').click()
    def temperatureMeasurement(self,x,y,x0=0,y0=0,mode='MULTI'):
        '''
        温度测量控件:
        对该模块的测试点：
        1.按钮通用状态测试：未选中状态、选中状态、悬停状态。方案：检查图片名
        2.选中状态的有效性：单点模式、多点模式、单区域模式。方案：检查选中后的功能是否匹配
        3.测温准确度检查：返回正常值、值是否正确（建议通过接口直接检查）
        4.返回值检查（建议通过接口测试检测）

        *备注：控件的(0,0)坐标位置在控件的左上角
        '''

        #温度测量入口
        self.driver.find_element_by_id('btn_Set_cw').click()
        #操作模式选择
        if 'MULTI'==mode:
            #多点模式操作
            self.driver.find_element_by_id('btn_cw_continue').click()  # 单点测温模式选择
            temp = self.driver.find_element_by_id('cavars')
            ActionChains(driver).move_to_element_with_offset(temp, x, y).click().perform()  # 确定点击位置
            time.sleep(10)

        elif 'SINGLE'==mode:
            #单点模式操作
            self.driver.find_element_by_id('btn_cw_single').click()   #单点测温模式选择
            temp=self.driver.find_element_by_id('cavars')
            ActionChains(driver).move_to_element_with_offset(temp,x,y).click().perform()  # 确定点击位置
            time.sleep(10)

        elif 'AREA'==mode:
            #区域模式
            self.driver.find_element_by_id('btn_cw_area').click()   #区域测温模式选择
            temp=self.driver.find_element_by_id('cavars')
            action=ActionChains(driver).move_to_element_with_offset(temp, x0, y0)  #选择起始位置
            action.click_and_hold().move_by_offset(x,y).release().perform()  #画矩形区域
            time.sleep(10)

        else:
            print('选择模式错误：必须为SINGLE、MULTI、AREA模式之一')
        #退出测温模式
        self.driver.find_element_by_id('btn_Set_cw').click()
    def getAlarmStatus(self,statusID):
        #内置两组状态变更流
        realAlarm=('新上报','已确认','已计划','检修中','已关闭','已取消')
        alarmStatusOn=[] #显示开启的状态
        alarmStatusDisplay=[] #显示当前展示的所有状态
        nMax=-1
        status=self.driver.find_element_by_id(statusID).find_elements_by_tag_name('li')
        for s in status:
            if s.is_displayed():
                alarmStatusDisplay.append(s.text)
                if  'li_status_out' not in s.get_attribute('class'):
                    n=realAlarm.index(s.text)
                    alarmStatusOn.append(s.text)
                    if nMax<n:
                        nMax=n
                #print(nMax, s.text)
        return realAlarm[nMax],alarmStatusOn,alarmStatusDisplay

if __name__=='__main__':
    #c=CreateDriver()
    url1='http://192.168.1.101:10032'
    url='http://192.168.1.101:10032/C3/PC/MAlarmMonitoring/MonitorAlarm3CForm4.htm?alarmid=F5434ad71669545d9b6ca276d9a9a55c2'
    driver=CreateDriver.getBrowserDriver()
    print(driver)
    driver.maximize_window()
    driver.get(url1)
    driver.find_element_by_id('username').send_keys('admin')
    driver.find_element_by_id('password').send_keys('cdgt@qwer')
    print(driver.find_element_by_xpath('/html/body/div[2]/div[2]/ul/li[2]').get_attribute('value'))
    print(driver.find_element_by_id('password').get_attribute('value'))
    driver.find_element_by_class_name("login_go").click()
    '''
    alarm=AlarmDetail(driver,url)
    time.sleep(1)
    alarm.confirm()
    alarm = AlarmDetail(driver, url)
    time.sleep(1)
    alarm.cancel()
    alarm = AlarmDetail(driver, url)
    time.sleep(1)
    alarm.export()
    alarm = AlarmDetail(driver, url)
    time.sleep(1)
    alarm.replay()
    alarm = AlarmDetail(driver, url)
    time.sleep(1)
    alarm.task()'''
    alarm = AlarmDetail(driver, url)
    time.sleep(1)
    print(alarm.getAlarmStatus('ul_status'))
    time.sleep(5)
    print(driver.find_element_by_xpath('//*[@id="TOP_three"]/div[2]/div[2]/ul/li[1]').text)
    driver.find_element_by_id('E_btnOk2').click()



    #alarm.confirm()
    driver.switch_to_frame('iframe_AlarmSure')
    table = TableBox.TrTd(driver, 'tb_sure')
    print(table.getInitData())
    #alarm.codeMenuTree('疑似跨中接触线燃弧','citySel','UL')
    #alarm.serverity('一级','Useverity')
    #alarm.textBoxWithSelect('线n',TEXT_INPUT,'UtxtDefect',prefix='UL')
    #alarm.getAlarmMes()
    #alarm.preData()
    #driver.find_element_by_id('hw').click()
    #alarm.temperatureMeasurement('AREA')
    #alarm.getCurve()
    #alarm