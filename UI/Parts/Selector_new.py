# _*_ coding=utf-8 _*_
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException, UnexpectedTagNameException
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
def relateID(driver,componentID):
    '''
    该函数主要解决组件输入区与选项区域之间的关联关系,主要通过id进行关联

    输入区：<button id='webElement' .../>
    选项区：<ul id >
    :param driver:
    :param componentID:
    :return:
    '''
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
#通用控件区
class OptionSelector(Select):
    '''
    该类继承自官方给定的Select类，增加了获取当前选项和所有选项的值的方法
    '''
    def __init__(self, webElement):
        '''
            初始化类，参数说明如下：
            :param webElement: 该控件关联文本框的ID（根据开发提供，所有控件必须操作ID）
         '''
        #初始化继承类
        Select.__init__(self,webElement)
        #self.myOption=webElement
    def getValue(self):
        #return self.myOption.get_attribute('value')
        return self.first_selected_option.get_attribute('value')
    def getAllOption(self):
        #options=self.myOption.find_elements_by_tag_name('option')
        options=self.options
        values=[]
        for o in options:
            values.append(o.text)
        return values

#特殊控件区
class AlarmCurveSelector(object):
    def __init__(self,webElement):
        '''
        关键点：div为webElement的定位，button为曲线输入区，ul为曲线下拉选择区
        <div id="divDropButton" class="btn-group" role="group" style="position: absolute; top: 0px; z-index: 1; left: 827px;">
                <button id="dropButton" type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" style="width: 133px; background-color: #1B1B1B;
                    color: White; background-image: none; text-shadow: none; border-color: #FFF;
                    border-width: 3px; border-radius: 7px;padding-left: 0;">
                    <span id="chartTitle">拉出值曲线</span> <span class="glyphicon glyphicon-chevron-down" style="color: White;"></span>
                </button>
                <ul class="dropdown-menu" style="min-width: 127px; width: 127px; background-color: #1B1B1B;border-color: #FFF;border-width: 3px;">
                    <li style="background-color: #1B1B1B; color: White; background-image: none; text-shadow: none;
                        border-color: #FFF; border-width: 5px; border-radius: 7px;">
                        <a id="wd" href="javascript:void(0);" style="color: White;">
                            温度曲线
                        </a>
                    </li>
                    <li>
                        <a id="lc" href="javascript:void(0);" style="color: White;">拉出值曲线</a>
                    </li>
                    <li><a id="dg" href="javascript:void(0);" style="color: White;">导高值曲线</a></li>
                    <li><a id="wdd" href="javascript:void(0);" style="color: White;">温度导高值曲线</a></li>
                </ul>
        </div>
        :param webElement:
        '''
        #该判断不太合理，需要进一步研究
        if webElement.tag_name.lower()!='div':
            raise UnexpectedTagNameException(
                "Select only works on <div> elements, not on <%s>" %webElement.tag_name)
        self._el = webElement
        #self._el.find_element_by_tag_name('button').click()

    def select_by_order(self, index):
        '''
        通过下拉选项从上致下的顺序选择相应的值
        :param index:选择1致选项总数
        :return:返回选择的值
        '''
        self._el.find_element_by_tag_name('button').click()
        n = 1
        options = self._el.find_element_by_tag_name('ul').find_elements_by_tag_name('a')
        #print(options)
        if len(options)<index:
            index=len(options)
            #加入日志说明
        if index<1:
            index=1
            # 加入日志说明
        for opt in options:
            if n == index:
                mytext=opt.text
                opt.click()
                return mytext
            n = n + 1

    def select_by_visible_text(self, text):
        """
            Deselect all a that have a value matching the argument. That is, when given "温度曲线" this
                            would deselect an option like:

                <a id="wd" href="javascript:void(0);" style="color: White;">温度曲线</a>

                :Args:
                    - value - The value to match against

            throws NoSuchElementException If there is no option with specisied value in SELECT
        """
        self._el.find_element_by_tag_name('button').click()
        matched=False
        options=self._el.find_element_by_tag_name('ul').find_elements_by_tag_name('a')
        #print(options)
        for opt in options:
            #print(opt.text,text)
            if opt.text.lower()==text.lower():
                opt.click()
                matched=True
                return matched
        if not matched:
            raise NoSuchElementException("Cannot locate option with value: %s" % text)

    def getValue(self):
        return self._el.find_element_by_id('chartTitle').text

    def getAllValue(self):
        self._el.find_element_by_tag_name('button').click()
        values=[]
        options=self._el.find_element_by_tag_name('ul').find_elements_by_tag_name('a')
        for opt in options:
            values.append(opt.text)
        self._el.find_element_by_tag_name('button').click()
        return values

class AlarmTypeSelector(object):  # TextBoxWithList
    '''
    应用范围：
        3C：报警类型选择
    '''
    def __init__(self, driver , id):
        '''
        初始化类，参数说明如下：
        '''
        self._dr=driver
        self._id=id
        if self._dr.find_element_by_id(self._id).tag_name.lower()!='input':
            raise UnexpectedTagNameException(
                "Select only works on <div> elements, not on <%s>" %self._dr.find_element_by_id(self._id).tag_name)
        self._el=self._dr.find_element_by_id(self._id)
        self._sid=relateID(self._dr,self._id)
        self._sel=self._dr.find_element_by_id(self._sid) #下拉列表元素区

    # 文本框支持直接输入
    def input_message(self, text, mode='a'):
        '''
        直接输入文本信息，但是必须支持该页面才能调用
        :param inputMes: 输入内容
        :param mode: 输入模式a代表追加（默认），c代表清除原有内容
        :return: 返回输入后控件的value
        '''
        # 判定mode是否合法
        if self._el.get_attribute('readonly')=='readonly':
            raise Exception("禁止输入！")
        if mode.lower() not in ('a', 'c'):
            raise Exception("mode只允许输入：a追加输入，c清除并输入")
        self._el.click()
        time.sleep(1)
        if mode == 'c':
            self._el.clear()
        self._el.send_keys(text)
        self._el.click()
        return self._el.get_attribute('value')

    def select_by_text(self, text):
        '''
        通过下拉选项从上致下的顺序选择相应的值
        :param index:选择1致选项总数
        :return:返回选择的值
        '''
        matched=False
        self._el.click()
        time.sleep(1)
        #self._sel.find_element_by_tag_name('a').click()
        options = self._sel.find_elements_by_tag_name('a')
        for opt in options:
            opText=opt.text
            if opText == text:
                opt.click()
                matched=True
                return opText
        if not matched:
            raise NoSuchElementException("Cannot locate option with value: %s" % text)

    def select_by_code(self, code):
        '''
        通过下拉选项从上致下的顺序选择相应的值
        :param index:选择1致选项总数
        :return:返回选择的值
        '''
        matched=False
        self._el.click()
        time.sleep(1)
        #self._sel.find_element_by_tag_name('a').click()
        options = self._sel.find_elements_by_tag_name('a')
        for opt in options:
            opCode=opt.get_attribute('code')
            opText=opt.text
            print(opCode,code)
            if opCode == code:
                opt.click()
                matched=True
                return opText
        if not matched:
            raise NoSuchElementException("Cannot locate option with value: %s" % code)

    def select_by_order(self, order):
        '''
        通过下拉选项从上致下的顺序选择相应的值
        :param index:选择1致选项总数
        :return:返回选择的值
        '''
        n = 1
        self._el.click()
        time.sleep(1)
        options = self._sel.find_elements_by_tag_name('a')
        if len(options)<order:
            order=len(options)
            #加入日志说明
        if order<1:
            order=1
            # 加入日志说明
        for opt in options:
            if n == order:
                opText=opt.text
                opt.click()
                return opText
            n = n + 1

    def getAllValue(self):
        '''
        获取下拉中的所有选项
        :return: 按字典方式返回
        '''
        ##ULcitySel > div:nth-child(1) > div.type1
        values = dict()
        self._el.click()
        time.sleep(1)
        groups = self._dr.find_elements_by_css_selector('#' + self._sid + ' > div')
        gn = 1
        for gp in groups:
            title = self._dr.find_element_by_css_selector('#' + self._sid + ' > div:nth-child('+str(gn)+') > div:nth-child(1)').find_element_by_tag_name('a').text
            values[title] = []
            lists = self._dr.find_element_by_css_selector('#' + self._sid + ' > div:nth-child('+str(gn)+') > div:nth-child(2)').find_elements_by_tag_name('a')
            for list in lists:
                values[title].append(list.text)
            gn+=1
        self._el.click()
        return values

    def getValue(self):
        '''
        主要用于获取页面加载初始状态下的文本框值，也可以返回任意时刻的文本框值
        :return: 文本框当前值
        '''
        return self._el.get_attribute('value')

    def clear(self):
        '''
        清除文本框中的所有信息
        :return:无返回值
        '''
        self._el.clear()

class AlarmDealSelector(object):
    '''
        应用范围：
            3C：报警分析、处理建议
    '''

    def __init__(self, driver, id):
        '''
        初始化类，参数说明如下：
        :param driver: 提供页面操作句柄，该句柄必须来自于webdriver
        :param componentID: 该控件关联文本框的ID（根据开发提供，所有控件必须操作ID）
        '''
        self._dr=driver
        self._id=str(id)
        if self._dr.find_element_by_id(self._id).tag_name.lower()!='input':
            raise UnexpectedTagNameException(
                "Select only works on <div> elements, not on <%s>" %self._dr.find_element_by_id(self._id).tag_name)
        self._el=self._dr.find_element_by_id(self._id)
        self._sid=relateID(self._dr,self._id)
        self._sel=self._dr.find_element_by_id(self._sid) #下拉列表元素区
    def input_message(self, text, mode='a'):
        '''
        直接输入文本信息，但是必须支持该页面才能调用
        :param text: 输入内容
        :param mode: 输入模式a代表追加（默认），c代表清除原有内容
        :return: 返回输入后控件的value
        '''
        # 判定mode是否合法
        if mode not in ('a', 'c'):
            raise Exception("模式(mode)选择错误，请输入'c'或者'a'")
        self._el.click()  # 打开文件下拉
        if mode == 'c':
            self._el.clear()
        self._el.send_keys(text)
        return self._el.get_attribute('value')
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

    def select_by_text(self, text):
        '''
        通过下拉选项从上致下的顺序选择相应的值
        :param index:选择1致选项总数
        :return:返回选择的值
        '''
        matched=False
        self._el.click()
        time.sleep(1)
        options = self._sel.find_elements_by_tag_name('a')
        for opt in options:
            opText=opt.text
            if opText == text:
                opt.click()
                matched=True
                return opText
        if not matched:
            raise NoSuchElementException("Cannot locate option with value: %s" % text)

    def select_by_order(self, order):
        '''
        通过下拉选项从上致下的顺序选择相应的值
        :param index:选择1致选项总数
        :return:返回选择的值
        '''
        n = 1
        self._el.click()
        time.sleep(1)
        options = self._sel.find_elements_by_tag_name('a')
        if len(options)<order:
            order=len(options)
            #加入日志说明
        if order<1:
            order=1
            # 加入日志说明
        for opt in options:
            if n == order:
                opText=opt.text
                opt.click()
                return opText
            n = n + 1

    def getAllValue(self):
        self._el.click()
        values=[]
        options=self._sel.find_elements_by_tag_name('a')
        for opt in options:
            values.append(opt.text)
        self._el.click()
        return values

    def getValue(self):
        '''
        主要用于获取页面加载初始状态下的文本框值，也可以返回任意时刻的文本框值
        :return: 文本框当前值
        '''
        return self._el.get_attribute('value')

    def clear(self):
        '''
        清除文本框中的所有信息
        :return:无返回值
        '''
        self._el.clear()

    def clearSelector(self):
        '''
        前置条件，进入了查询区域或者输入了查询信息
        :return: 返回True代表清除成功,False代表清除失败
        '''
        try:
            self._dr.find_element_by_xpath('//*[@id="' + self._sid + '"]/preceding-sibling::div[1]/a').click()
            return True
        except:
            return False

    def isReadOnly(self):
        '''
        判定是否文本框为只读模式
        :return: True代表返回只读，False代表非只读
        '''
        rd=self._el.get_attribute('readonly')
        if rd=="readonly" or rd or rd==None:
            return True
        else:
            return False

if __name__ == "__main__":
    url1 = 'http://183.203.132.154:9100'
    url = 'http://183.203.132.154:9100/C3/PC/MAlarmMonitoring/MonitorAlarm3CForm4.htm?alarmid=F23dcab41450047f2b8c88be58e695a22'
    # driver=CreateDriver.getBrowserDriver()
    driver = webdriver.Chrome()
    #print(driver)
    driver.maximize_window()
    driver.get(url1)
    driver.find_element_by_id('username').send_keys('admin')
    driver.find_element_by_id('password').send_keys('b1f66')
    driver.find_element_by_class_name("login_go").click()
    driver.get(url)
    time.sleep(3)
    '''
    #<OptionSelector>测试脚本
    driver.find_element_by_id('E_btnOk2').click()
    time.sleep(3)
    driver.switch_to.frame('iframe_AlarmSure')
    alarm=AlarmTypeSelector(driver,'citySel')
    time.sleep(2)
    print(alarm.getAllValue())
    time.sleep(2)
    print(alarm.getValue())
    time.sleep(2)
    print(alarm.input_message("疑似线夹燃弧"))
    time.sleep(2)
    print(alarm.select_by_code("FXYSGJYQLF"))
    time.sleep(2)
    print(alarm.select_by_order(5))
    time.sleep(2)
    print(alarm.select_by_text("疑似跨中接触线燃弧"))
    '''
    '''
    #<AlarmCurveSelector>测试脚本
    se=AlarmCurveSelector(driver.find_element_by_id('divDropButton'))
    print('------------select_by_visible_text("温度曲线")-----------------')
    se.select_by_visible_text('温度曲线')
    print(se.getValue())
    time.sleep(1)
    print('------------select_by_visible_text("拉出值曲线")-----------------')
    se.select_by_visible_text('拉出值曲线')
    print(se.getValue())
    time.sleep(1)
    print('------------select_by_index(-1)-----------------')
    print(se.select_by_index(-1))
    print(se.getValue())
    time.sleep(1)
    print('------------select_by_index(10)-----------------')
    print(se.select_by_index(10))
    print(se.getValue())
    time.sleep(1)
    print('------------select_by_index(2)-----------------')
    print(se.select_by_index(2))
    print(se.getValue())
    print("OK")
    time.sleep(1)
    print(se.getAllValue())
    '''

    '''
    #<OptionSelector>测试脚本
    driver.find_element_by_id('E_btnOk2').click()

    time.sleep(3)
    driver.switch_to.frame('iframe_AlarmSure')
    print("修改之前的值：",OptionSelector(driver.find_element_by_id('Useverity')).getValue())
    #print(OptionSelector(driver.find_element_by_id('Useverity')).all_selected_options)
    #print(OptionSelector(driver.find_element_by_id('Useverity')).first_selected_option)
    #print(OptionSelector(driver.find_element_by_id('Useverity')).options)
    OptionSelector(driver.find_element_by_id('Useverity')).select_by_visible_text('X级')
    print("修改之后的值：",OptionSelector(driver.find_element_by_id('Useverity')).getValue())
    #time.sleep(2)
    print("全部选项：",OptionSelector(driver.find_element_by_id('Useverity')).getAllOption())
    '''
    wait=input("输入任意字符退出：")
    driver.close()