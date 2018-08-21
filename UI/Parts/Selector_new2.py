# _*_ coding=utf-8 _*_
from selenium.webdriver.common.keys import Keys

from Parts.BaseObject import BaseSelector
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException, UnexpectedTagNameException
from log.TestLogBook import run_log as logger
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

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
# 输入区与选项区之间的关联关系
dict_relate_id = {'UtxtDefect': "ULUtxtDefect", 'citySel': "ULcitySel", 'UtxtAdvice': "ULUtxtAdvice", 'DefectMark': "ULDefectMark",
                  'SceneSample_Sure': "droup_SceneSample_Sure", 'button.ui-multiselect.ui-widget.ui-state-default.ui-corner-all': 'div.ui-multiselect-menu.ui-widget.ui-widget-content.ui-corner-all'}

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


# 通用控件区
# 该类继承自官方给定的Select类，增加了获取当前选项和所有选项的值的方法

class OptionSelector(Select):

    def __init__(self, webElement):
        '''
            初始化类，参数说明如下：
            :param webElement: 该控件关联文本框的ID（根据开发提供，所有控件必须操作ID）
         '''
        # 初始化继承类
        Select.__init__(self,webElement)
        # self.myOption=webElement

    # 获取当前选项的值
    def getValue(self):
        #return self.myOption.get_attribute('value')
        return self.first_selected_option.get_attribute('value')

    # 获取所有选项的值
    def getAllOption(self):
        #options=self.myOption.find_elements_by_tag_name('option')
        options=self.options
        values=[]
        for o in options:
            values.append(o.text)
        return values

# 特殊控件区
# 报警曲线
class AlarmCurveSelector(BaseSelector):
    def __init__(self,webElement):
        # 关键点：div为webElement的定位，button为曲线输入区，ul为曲线下拉选择区
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
        # 该判断不太合理，需要进一步研究
        # lower()转换成 小写
        if webElement.tag_name.lower()!='div':
            raise UnexpectedTagNameException(
                "Select only works on <div> elements, not on <%s>" % webElement.tag_name)
        self. _elt = webElement
        BaseSelector.__init__(self, self._text_el, self._options_el)

    @property
    def _options_el(self):
        self._text_el.click()
        options = self._text_el.find_element_by_tag_name('ul').find_elements_by_tag_name('a')
        self._text_el.click()
        return options

    @property
    def _text_el(self):
        return self._elt
        #return self._el


    def get_value(self):
        #重写了获取当前选择值的方法
        return self._text_el.find_element_by_id('chartTitle').text

    def select_by_index(self, code):
       pass

# 报警类型选择
class AlarmTypeSelector(BaseSelector):  # TextBoxWithList
    '''
    应用范围：
        3C：报警类型选择
    '''
    def __init__(self,driver,id):
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
        self._dr = driver
        self._id = id
        if self._dr.find_element_by_id(self._id).tag_name.lower()!='input':
            raise UnexpectedTagNameException(
                "Select only works on <div> elements, not on <%s>" %self._dr.find_element_by_id(self._id).tag_name)
        BaseSelector.__init__(self,self._text_el,self._options_el)

    @property
    def _options_el(self):
        self._text_el.click()
        # 通过选择输入框的ＩＤ关联选项区域并找到选项区域ＩＤ
        self._sid = dict_relate_id[self._id]
        # self._sid = relateID(self._dr, self._id)
        options = self._dr.find_element_by_id(self._sid).find_elements_by_tag_name('a')
        self._text_el.click()
        return options

    @property
    def _text_el(self):
        return self._dr.find_element_by_id(self._id)

    # 文本框支持直接输入
    def input_message(self, text, mode='a'):
        '''
        直接输入文本信息，但是必须支持该页面才能调用
        :param inputMes: 输入内容
        :param mode: 输入模式a代表追加（默认），c代表清除原有内容
        :return: 返回输入后控件的value
        '''
        # 判定mode是否合法
        if self._text_el.get_attribute('readonly')=='readonly':
            raise Exception("禁止输入！")
        if mode.lower() not in ('a', 'c'):
            raise Exception("mode只允许输入：a追加输入，c清除并输入")
        self._text_el.click()
        if mode == 'c':
            self.clear()
        self._text_el.send_keys(text)
        self._text_el.click()
        return self._text_el.get_attribute('value')

    def get_options(self):
        '''
        获取下拉中的所有选项
        :return: 按字典方式返回
        '''
        ##ULcitySel > div:nth-child(1) > div.type1
        values = dict()
        self._text_el.click()
        groups = self._dr.find_elements_by_css_selector('#' + self._sid + ' > div')
        gn = 1
        for gp in groups:
            title = self._dr.find_element_by_css_selector('#' + self._sid + ' > div:nth-child('+str(gn)+') > div:nth-child(1)').find_element_by_tag_name('a').text
            values[title] = []
            lists = self._dr.find_element_by_css_selector('#' + self._sid + ' > div:nth-child('+str(gn)+') > div:nth-child(2)').find_elements_by_tag_name('a')
            for list in lists:
                values[title].append(list.text)
            gn+=1
        self._text_el.click()
        return values

    def clear(self):
        '''
        清除文本框中的所有信息
        :return:无返回值
        '''
        self._text_el.clear()

    def isReadOnly(self):
        '''
        判定是否文本框为只读模式
        :return: True代表返回只读，False代表非只读
        '''
        rd=self._text_el.get_attribute('readonly')
        if rd=="readonly" or rd or rd==None:
            return True
        else:
            return False


# 处理意见、报警分析（两者下拉框类似）
class AlarmDealSelector(BaseSelector):
    """
        应用范围：
            3C：报警分析、处理建议
    """
    def __init__(self, driver, id):
        """
        :Args:
            - driver -
            - id -  the id of the AlarmDealSelector
        """
        # 该判断不太合理，需要进一步研究
        self._dr = driver
        self._id = id
        if self._dr.find_element_by_id(self._id).tag_name.lower() != 'textarea':
            raise UnexpectedTagNameException(
                "Select only works on <div> elements, not on <%s>" % self._dr.find_element_by_id(self._id).tag_name)
        BaseSelector.__init__(self, self._text_el, self._options_el)

    @property
    def _options_el(self):
        # self._text_el.click()  # 弹出下拉列表（不弹出列表，也能获取到option）
        # 通过选择输入框的ID关联选项区域并找到选项区域ID
        self._sid = dict_relate_id[self._id]
        # self._sid = relateID(self._dr, self._id)
        options = self._dr.find_element_by_id(self._sid).find_elements_by_tag_name('a')
        # self._text_el.click()  # 收起下拉列表
        return options

    @property
    def _text_el(self):
        # 通过id找到元素
        return self._dr.find_element_by_id(self._id)

    def input_message_text(self, text, mode='a'):
        """
        直接输入文本信息，但是必须支持该页面才能调用
        :param text: 输入内容
        :param mode: 输入模式a代表追加（默认），c代表清除原有内容
        :return: 返回输入后控件的value
        """
        # 判定mode是否合法
        if mode not in ('a', 'c'):
            raise Exception("模式(mode)选择错误，请输入'c'或者'a'")
        self._text_el.click()  # 打开文件下拉
        if mode == 'c':
            self.clear()
        self._text_el.send_keys(text)
        return self._text_el.get_attribute('value')


    def clear(self):
        '''
        清除文本框中的所有信息
        :return:无返回值
        '''
        self._text_el.clear()

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
        rd=self._text_el.get_attribute('readonly')
        if rd == "readonly" or rd or rd==None:
            return True
        else:
            return False

    def input_key_search(self, keyword):
        """
        在搜索框输入关键字
        :param keyword: 输入的关键字
        :return: 与关键字模糊查询匹配的选项列表的值
        """
        time.sleep(1)
        self._text_el.click()  # 点击文本框，弹出搜索框
        time.sleep(1)
        try:
            search_ele = self._dr.find_element_by_xpath('//*[@id="' + self._sid + '"]/preceding-sibling::div[1]/input')  # 找到搜索框
            time.sleep(1)
            search_ele.click()  # 点击搜索框
            time.sleep(1)
            search_ele.clear()
            search_ele.send_keys(keyword)  # 输入搜索关键字
            time.sleep(1)
            # 将查询结果保存到search_options-----这个地方不太合理，后面修改(DefectMarkSelector类中该地方已做优化，请参考)
            search_options = self._dr.find_element_by_xpath('//ul[@id="' + self._sid + '"]').find_elements_by_partial_link_text(keyword)
            return search_options
        except:
            print("没有找到搜索框，或对其操作出现问题")

    def select_key_search_order(self, keyword, order):
        """
        在搜索框输入关键字：keyword，然后通过order（顺序1，2, 3....）选择对应的选项
        :param keyword:string
        :param order:
        :return:
        """
        search_options = self.input_key_search(keyword)
        # 根据order选择对应的选项：
        n = 1
        if len(search_options) == 0:
            print("所输入关键字：", keyword, "没有查询到选项")
        if len(search_options) < order:
            order = len(search_options)
            # 加入日志说明
        if order < 1:
            order = 1
            # 加入日志说明
        for opt in search_options:
            if n == order:
                opText = opt.text
                opt.click()
                return opText
            n = n + 1


    def input_key_search_text(self, keyword, text):
        """
        在搜索框输入关键字：keyword，然后通过文本选择对应的选项
        :param keyword:
        :param order:
        :return:
        """
        search_options = self.input_key_search(keyword)
        # 根据text选择对应的选项：
        matched = False
        for opt in search_options:
            opText = opt.text.strip()
            # print(opText,text)
            if opText == text.strip():
                opt.click()
                matched = True
                return opText
        if not matched:
            raise NoSuchElementException("Cannot locate option with value: %s" % text)


# 导出下拉列表
class ExportSelector(BaseSelector):
    '''
        应用范围：
            3C：详情导出、详情重解析、3C列表页导出
        说明：需要自己找到该功能的定位
    '''
    def __init__(self, webdriver):
        #该判断不太合理，需要进一步研究
        self._web=webdriver
        if self._web.tag_name.lower()!='div':
            raise UnexpectedTagNameException(
                "Select only works on <div> elements, not on <%s>" %self._web.tag_name)
        BaseSelector.__init__(self,self._text_el,self._options_el)
    @property
    def _options_el(self):
        self._text_el.click()
        options = self._web.find_element_by_tag_name('ul').find_elements_by_tag_name('a')
        self._text_el.click()
        return options

    @property
    def _text_el(self):
        #直接获取第一个a标签作为按钮
        return self._web.find_element_by_tag_name('a')

    def select_by_index(self, code):
        #屏蔽当前方法
        pass

    def get_button_name(self):
        #获取按钮的名称
        return self._text_el.text

# 缺陷标志下拉复选框
class DefectMarkSelector(BaseSelector):
    """        应用范围：缺陷标志   """

    def __init__(self, driver, id):
        """
        :Args:
            - driver -
            - id -  the id of the DefectMarkSelector
        """
        # 该判断不太合理，需要进一步研究
        self._dr = driver
        self._id = id
        if self._dr.find_element_by_id(self._id).tag_name.lower() != 'input':
            raise UnexpectedTagNameException(
                "Select only works on <div> elements, not on <%s>" % self._dr.find_element_by_id(self._id).tag_name)
        BaseSelector.__init__(self, self._text_el, self._options_el)

    @property
    def _options_el(self):
        # self._text_el.click()  # 弹出下拉列表（不弹出列表，也能获取到option）
        # 通过选择输入框的ID关联选项区域并找到选项区域ID
        self._sid = dict_relate_id[self._id]
        # self._sid = relateID(self._dr, self._id)
        options = self._dr.find_element_by_id(self._sid).find_elements_by_tag_name('li')
        # self._text_el.click()  # 收起下拉列表
        return options

    @property
    def _text_el(self):
        # 通过id找到元素
        return self._dr.find_element_by_id(self._id)

    def _setSelected(self, option):
        """
        将未选选项置为选择状态
        :param option:
        :return:
        """
        check_ele = option.find_element_by_xpath('./span[2]')      # 找到对应复选框
        if check_ele.get_attribute('class') == 'button chk checkbox_false_full':     # 如果复选框时未选择状态，则点击，否则抛出异常
            check_ele.click()
        else:
            raise Exception("该选项是已选中状态：%s" % option.text)

    def _unsetSelected(self, option):
        """
        将已选选项置为未选状态
        :param option:
        :return:
        """
        check_ele = option.find_element_by_xpath('./span[2]')
        if check_ele.get_attribute('class') == 'button chk checkbox_true_full':
            check_ele.click()
        else:
            raise Exception("该选项是未选中状态：%s" % option.text)

    def _select_by_order_list(self, options, orderlist):
        """
        选择下拉列表（根据order（下拉列表选项顺序，从1开始）选择）
        :param orderlist: list[1,2,3]
        :return:opTextList
        注意：如果选项是已选择状态，则会抛出异常
        """
        opTextList = []
        for order in orderlist:
            n = 1
            if len(options) < order:
                order = len(options)
                logger.warning("输入order大于选项总数，将order置为选项总数")
            if order < 1:
                order = 1
                logger.warning("输入order小于1，将order置为1")
            for opt in options:
                if n == order:
                    self._setSelected(opt)
                    opTextList.append(opt.text)
                    break
                n = n + 1
        return opTextList

    def _select_by_text_list(self, options, textlist):
        """
        选择下拉列表（根据order（下拉列表选项顺序，从1开始）选择）
        :param   options     textlist: list['','','']
        :return:opTextList
        注意：如果选项是已选择状态，则会抛出异常
        """
        opTextList = []
        for text in textlist:
            matched = False
            for opt in options:
                opText = opt.text.strip()
                if opText == text.strip():
                    self._setSelected(opt)
                    opTextList.append(opText)
                    matched = True
                    break
            if not matched:
                raise NoSuchElementException("Cannot locate option with value: %s" % text)
        return opTextList

    def select_by_order(self, orderlist):
        """
        选择下拉列表（根据order（下拉列表选项顺序，从1开始）选择--未输入关键字）
        :param orderlist: list[1,2,3]
        :return:
        选择选项并确认后，再次进入该页面，文本框中保存了之前选择的内容，但是下拉选项没有默认勾选，再次选择其他选项，会覆盖之前选项
        """
        logger.info("通过元素在HTML中的顺序orderlist[]设置选项")
        time.sleep(1)
        self._el.click()
        time.sleep(1)
        opTextList = self._select_by_order_list(self._options, orderlist)
        self._el.click()   # 收起下拉列表
        logger.info("所设置的选项为：")
        logger.info(opTextList)

    def select_by_text(self, textlist):
        """
        选择下拉列表（根据文本选择--未输入关键字）
        :param textlist: list['', '']
        :return:opTextList
        选择选项并确认后，再次进入该页面，文本框中保存了之前选择的内容，但是下拉选项没有默认勾选，再次选择其他选项，会覆盖之前选项
        """
        logger.info("通过选项文本设置选项")
        time.sleep(1)
        self._el.click()
        time.sleep(1)
        opTextList = self._select_by_text_list(self._options_el, textlist)
        logger.info("所设置的选项为：")
        logger.info(opTextList)
        self._el.click()  # 收起下拉列表
        return opTextList

    def deselect_by_order_list(self, orderlist):
        """
        取消选择（根据order（下拉列表选项顺序，从1开始）选择--未输入关键字）
        :param orderlist: list[1,2,3]
        :return:opTextList
        注意：如果选项是未选择状态，则会抛出异常
        """
        logger.info("通过元素在HTML中的顺序orderlist[]设置选项（取消已选选项）")
        time.sleep(1)
        self._el.click()
        time.sleep(1)
        opTextList = []
        for order in orderlist:
            n = 1
            if len(self._options) < order:
                order = len(self._options)
                logger.warning("输入order大于选项总数，将order置为选项总数")
            if order < 1:
                order = 1
                logger.warning("输入order小于1，将order置为1")
            for opt in self._options:
                if n == order:
                    self._unsetSelected(opt)
                    opTextList.append(opt.text)
                    break
                n = n + 1
        logger.info("所取消的选项为：")
        logger.info(opTextList)
        self._el.click()   # 收起下拉列表
        return opTextList

    def deselect_by_text_list(self, textlist):
        """
        取消选择（根据文本取消--未输入关键字）
        :param textlist: list['', '']
        :return:opTextList
        """
        logger.info("通过选项文本设置选项（取消已选选项）")
        time.sleep(1)
        self._el.click()
        time.sleep(1)
        opTextList = []
        for text in textlist:
            matched = False
            for opt in self._options:
                opText = opt.text.strip()
                if opText == text.strip():
                    self._unsetSelected(opt)
                    opTextList.append(opText)
                    matched = True
                    break
            if not matched:
                raise NoSuchElementException("Cannot locate option with value: %s" % text)
        logger.info("所取消的选项为：")
        logger.info(opTextList)
        self._el.click()  # 收起下拉列表
        return opTextList

    def get_allselected(self):
        """
        获取下拉列表中，已经选中的选项，并返回一个list（这个值和文本框中的值，不一定是一样的）
        :return: values[]
        """
        time.sleep(1)
        self._el.click()
        time.sleep(1)
        logger.info("获取下拉列表中，已经选中的选项：")
        values = []
        for opt in self._options:
            check_ele = opt.find_element_by_xpath('./span[2]')  # 找到对应复选框
            if  check_ele.get_attribute('class') == 'button chk checkbox_true_full':   # 保存标示为true的元素
                values.append(opt.text.strip())
        self._el.click()
        logger.info(values)
        return values

    def deselect_all(self):
        """
        取消所有已经选择的选项
        :return:
        """
        logger.info("取消所有已经选择的选项")
        Selected = self.get_allselected()
        self.deselect_by_text_list(Selected)

    def clear_button_text(self):
        """
        清除文本框中的所有信息，
        :return:无返回值
        """
        logger.info("清除文本框中的所有信息")
        self._dr.find_element_by_xpath('//*[@id="' + self._id + '"]/following-sibling::a').click()

    def clear_button_search(self):
        """
        清除搜索框中的所有信息，
        前置条件，进入了查询区域或者输入了查询信息
        :return:无返回值
        """
        logger.info("清除搜索框中的所有信息")
        self._dr.find_element_by_xpath('//*[@id="' + self._sid + '"]/preceding-sibling::div/a').click()

    def input_key_search(self, keyword):
        """
        在搜索框输入关键字
        备注：该方法同报警分析类中的该方法完全一致，后期可优化
        :param keyword: 输入的关键字
        :return: 与关键字模糊查询匹配的选项列表的值
        """
        time.sleep(1)
        self._text_el.click()  # 点击文本框，弹出搜索框
        time.sleep(1)
        try:
            search_ele = self._dr.find_element_by_xpath('//*[@id="' + self._sid + '"]/preceding-sibling::div[1]/input')  # 找到搜索框
            time.sleep(1)
            search_ele.click()  # 点击搜索框
            time.sleep(1)
            search_ele.clear()
            search_ele.send_keys(keyword)  # 输入搜索关键字
            time.sleep(1)
            search_options=[]
            """
            将查询结果保存到search_options
            本来想根据style直接定位元素，但是搜索结果中，显示元素style为空（通过print打印属性值为空），只能先找到style属性为display: none;（不展示的元素）
            再排除这些元素，即得到显示的元素，即搜索结果
            """
            # search_options0 = self._dr.find_element_by_xpath('//ul[@id="' + self._sid + '"]').find_element_by_xpath('./li[4]')
            # 打印style，显示为空
            # print("style为：", search_options0.get_attribute("style"))
            search_options_false = self._dr.find_element_by_xpath('//ul[@id="' + self._sid + '"]').find_elements_by_xpath("./li[@style='display: none;']")
            for opt in self._options_el:
                if opt in search_options_false:
                    pass
                else:
                    search_options.append(opt)
            return search_options
        except:
            logger.error("没有找到搜索框，或对其操作出现问题")

    def select_key_search_order(self, keyword, orderlist):
        """
        在搜索框输入关键字：keyword，然后通过orderlist（顺序1，2, 3....）选择对应的选项
        :param keyword:string
        :param order:[1,2,3]
        :return:
        """
        logger.info('在搜索框中输入关键字, 并根据orderlist选择对应选项')
        search_options = self.input_key_search(keyword)
        if len(search_options) == 0:
            logger.warning("关键字没有对应搜索结果")
        else:
            self._select_by_order_list(search_options, orderlist)
        self._text_el.click()  # 点击文本框，收起搜索框

    def select_key_search_text(self, keyword, textlist):
        """
        在搜索框输入关键字：keyword，然后通过文本选择对应的选项
        :param keyword:
        :param textlist:
        :return:
        """
        logger.info('在搜索框中输入关键字, 并根据textlist选择对应选项')
        search_options = self.input_key_search(keyword)
        if len(search_options) == 0:
            logger.warning("关键字没有对应搜索结果")
        else:
            self._select_by_text_list(search_options, textlist)
        self._text_el.click()  # 点击文本框，收起搜索框

# 场景样本列表复选框
class SceneSampleSelector(BaseSelector):
    """        应用范围：场景样本   """

    def __init__(self, driver, id):
        """
        :Args:
            - driver -
            - id -  the id of the DefectMarkSelector
        """
        # 该判断不太合理，需要进一步研究
        self._dr = driver
        self._id = id
        if self._dr.find_element_by_id(self._id).tag_name.lower() != 'textarea':
            raise UnexpectedTagNameException(
                "Select only works on <div> elements, not on <%s>" % self._dr.find_element_by_id(self._id).tag_name)
        BaseSelector.__init__(self, self._text_el, self._options_el)

    @property
    def _options_el(self):
        # self._text_el.click()  # 弹出下拉列表（不弹出列表，也能获取到option）
        # 通过选择输入框的ID关联选项区域并找到选项区域ID
        self._sid = dict_relate_id[self._id]
        # self._sid = relateID(self._dr, self._id)
        options = self._dr.find_element_by_id(self._sid).find_elements_by_xpath('./div[2]/span')
        # self._text_el.click()  # 收起下拉列表
        return options

    @property
    def _text_el(self):
        # 通过id找到元素
        return self._dr.find_element_by_id(self._id)

    def _setSelected(self, option):
        """
        将未选选项置为选择状态
        :param option:
        :return:
        """
        if option.get_attribute('class') != 'checkSpan':     # 如果复选框时未选择状态，则点击，否则抛出异常
            option.click()
        else:
            raise Exception("该选项是已选中状态：%s" % option.text)

    def _unsetSelected(self, option):
        """
        将已选选项置为未选状态
        :param option:
        :return:
        """
        if option.get_attribute('class') == 'checkSpan':
            option.click()
        else:
            raise Exception("该选项是未选中状态：%s" % option.text)

    def _select_by_order_list(self, options, orderlist):
        """
        选择下拉列表（根据order（下拉列表选项顺序，从1开始）选择）
        :param orderlist: list[1,2,3]
        :return:opTextList
        注意：如果选项是已选择状态，则会抛出异常
        """
        opTextList = []
        for order in orderlist:
            n = 1
            if len(options) < order:
                order = len(options)
                logger.warning("输入order大于选项总数，将order置为选项总数")
            if order < 1:
                order = 1
                logger.warning("输入order小于1，将order置为1")
            for opt in options:
                if n == order:
                    self._setSelected(opt)
                    opTextList.append(opt.text)
                    break
                n = n + 1
        return opTextList

    def _select_by_text_list(self, options, textlist):
        """
        选择下拉列表（根据order（下拉列表选项顺序，从1开始）选择）
        :param   options     textlist: list['','','']
        :return:opTextList
        注意：如果选项是已选择状态，则会抛出异常
        """
        opTextList = []
        for text in textlist:
            matched = False
            for opt in options:
                opText = opt.text.strip()
                if opText == text.strip():
                    self._setSelected(opt)
                    opTextList.append(opText)
                    matched = True
                    break
            if not matched:
                raise NoSuchElementException("Cannot locate option with value: %s" % text)
        return opTextList

    def select_by_order(self, orderlist):
        """
        选择下拉列表（根据order（下拉列表选项顺序，从1开始）选择--未输入关键字）
        :param orderlist: list[1,2,3]
        :return:
        """
        logger.info("通过元素在HTML中的顺序orderlist[]设置选项")
        time.sleep(1)
        self._el.click()
        time.sleep(1)
        opTextList = self._select_by_order_list(self._options, orderlist)
        self._el.click()   # 收起下拉列表
        logger.info("所设置的选项为：")
        logger.info(opTextList)

    def select_by_text(self, textlist):
        """
        选择下拉列表（根据文本选择--未输入关键字）
        :param textlist: list['', '']
        :return:opTextList
        """
        logger.info("通过选项文本设置选项")
        time.sleep(1)
        self._el.click()
        time.sleep(1)
        opTextList = self._select_by_text_list(self._options_el, textlist)
        logger.info("所设置的选项为：")
        logger.info(opTextList)
        self._el.click()  # 收起下拉列表
        return opTextList

    def get_allselected(self):
        """
        获取下拉列表中，已经选中的选项，并返回一个list（这个值和文本框中的值，不一定是一样的）
        :return: values[]
        """
        time.sleep(1)
        self._el.click()
        time.sleep(1)
        logger.info("获取下拉列表中，已经选中的选项：")
        values = []
        for opt in self._options:
            if  opt.get_attribute('class') == 'checkSpan':   # 保存标示为true的元素
                values.append(opt.text.strip())
        self._el.click()
        logger.info(values)
        return values

    def deselect_by_order_list(self, orderlist):
        """
        取消选择（根据order（下拉列表选项顺序，从1开始）选择--未输入关键字）
        :param orderlist: list[1,2,3]
        :return:opTextList
        注意：如果选项是未选择状态，则会抛出异常
        """
        logger.info("通过元素在HTML中的顺序orderlist[]设置选项（取消已选选项）")
        time.sleep(1)
        self._el.click()
        time.sleep(1)
        opTextList = []
        for order in orderlist:
            n = 1
            if len(self._options) < order:
                order = len(self._options)
                logger.warning("输入order大于选项总数，将order置为选项总数")
            if order < 1:
                order = 1
                logger.warning("输入order小于1，将order置为1")
            for opt in self._options:
                if n == order:
                    self._unsetSelected(opt)
                    opTextList.append(opt.text)
                    break
                n = n + 1
        logger.info("所取消的选项为：")
        logger.info(opTextList)
        self._el.click()   # 收起下拉列表
        return opTextList

    def deselect_by_text_list(self, textlist):
        """
        取消选择（根据文本取消--未输入关键字）
        :param textlist: list['', '']
        :return:opTextList
        """
        logger.info("通过选项文本设置选项（取消已选选项）")
        time.sleep(1)
        self._el.click()
        time.sleep(1)
        opTextList = []
        for text in textlist:
            matched = False
            for opt in self._options:
                opText = opt.text.strip()
                if opText == text.strip():
                    self._unsetSelected(opt)
                    opTextList.append(opText)
                    matched = True
                    break
            if not matched:
                raise NoSuchElementException("Cannot locate option with value: %s" % text)
        logger.info("所取消的选项为：")
        logger.info(opTextList)
        self._el.click()  # 收起下拉列表
        return opTextList

    def deselect_all(self):
        """
        取消所有已经选择的选项
        :return:
        """
        logger.info("取消所有已经选择的选项")
        Selected = self.get_allselected()
        self.deselect_by_text_list(Selected)

    def input_key_search(self, keyword):
        """
        在搜索框输入关键字
        :param keyword: 输入的关键字
        :return: 与关键字模糊查询匹配的选项列表的值
        """
        time.sleep(1)
        self._text_el.click()  # 点击文本框，弹出搜索框
        time.sleep(1)
        try:
            search_ele = self._dr.find_element_by_xpath('//*[@id="' + self._sid + '"]/div[1]/input')  # 找到搜索框
            time.sleep(1)
            search_ele.click()  # 点击搜索框
            time.sleep(1)
            search_ele.clear()
            search_ele.send_keys(keyword)  # 输入搜索关键字
            time.sleep(1)
            # 将查询结果保存到search_options-----先找到没有显示的search_options_false，在找显示的search_options
            search_options = []
            search_options_false = self._dr.find_elements_by_xpath('//*[@id="' + self._sid + '"]/div[2]/span[@style="display: none;"]')
            for opt in self._options_el:
                if opt in search_options_false:
                    pass
                else:
                    search_options.append(opt)
            return search_options
        except:
            logger.error("没有找到搜索框，或对其操作出现问题")

    def select_key_search_order(self, keyword, orderlist):
        """
        在搜索框输入关键字：keyword，然后通过orderlist（顺序1，2, 3....）选择对应的选项
        :param keyword:string
        :param order:[1,2,3]
        :return:
        """
        logger.info('在搜索框中输入关键字, 并根据orderlist选择对应选项')
        search_options = self.input_key_search(keyword)
        if len(search_options) == 0:
            logger.warning("关键字没有对应搜索结果")
        else:
            self._select_by_order_list(search_options, orderlist)
        self._text_el.click()  # 点击文本框，收起搜索框

    def select_key_search_text(self, keyword, textlist):
        """
        在搜索框输入关键字：keyword，然后通过文本选择对应的选项
        :param keyword:
        :param textlist:
        :return:
        """
        logger.info('在搜索框中输入关键字, 并根据textlist选择对应选项')
        search_options = self.input_key_search(keyword)
        if len(search_options) == 0:
            logger.warning("关键字没有对应搜索结果")
        else:
            self._select_by_text_list(search_options, textlist)
        self._text_el.click()  # 点击文本框，收起搜索框

    def clear_button(self):
        """
        清除搜索框中的所有信息，
        前置条件，进入了查询区域或者输入了查询信息
        :return:无返回值
        """
        logger.info("清除搜索框中的所有信息")
        self._dr.find_element_by_xpath('//*[@id="' + self._sid + '"]/div[1]/a').click()

    def shutdown_button(self):
        """
        右上角关闭按钮，前置条件，打开了列表
        :return:无返回值
        """
        logger.info("点击关闭按钮")
        self._dr.find_element_by_xpath('//*[@id="' + self._sid + '"]/img').click()

# 时间控件
class TimeSelector(object):
    def __init__(self, driver, id):
        self._dr = driver
        self._id = id

    def settime(self, time):
        timetext = self._dr.find_element_by_id(self._id)
        timetext.click()
        timetext.clear()
        timetext.send_keys(time)
        timetext.send_keys(Keys.ENTER)

    def button_clear(self):
        pass

    def button_today(self):
        pass

    def button_confirm(self):
        pass

    def catch_alert(self):
        """
        捕获输入异常数据时的提示信息
        :return: 弹框中的提示信息
        """
        try:
            alert = self._dr.switch_to.alert
            alert.text
            return alert.text
        except:
            logger.info("没有捕获到弹框")

# 缺陷类型选择（同点对比）
class DefectTypesSelector(BaseSelector):
    def __init__(self,driver,id):
        #该判断不太合理，需要进一步研究
        self._dr = driver
        self._id = id
        if self._dr.find_element_by_id(self._id).tag_name.lower()!='input':
            raise UnexpectedTagNameException(
                "Select only works on <div> elements, not on <%s>" %self._dr.find_element_by_id(self._id).tag_name)
        BaseSelector.__init__(self,self._text_el,self._options_el)

    @property
    def _options_el(self):
        #self._text_el.click()
        # 通过选择输入框的ＩＤ关联选项区域并找到选项区域ＩＤ
        self._sid = dict_relate_id[self._id]
        # self._sid = relateID(self._dr, self._id)
        options = self._dr.find_element_by_id(self._sid).find_elements_by_tag_name('li')
        #self._text_el.click()
        return options

    @property
    def _text_el(self):
        return self._dr.find_element_by_id(self._id)

    def _setSelected(self, option):
        """
        将未选选项置为选择状态（仅限于三级选项）
        :param option:
        :return:
        """
        time.sleep(1)
        check_ele = option.find_element_by_xpath('./span[2]')      # 找到对应复选框
        if check_ele.get_attribute('class') == 'button chk checkbox_false_full':     # 如果复选框时未选择状态，则点击，否则抛出异常
            check_ele.click()
        else:
            raise Exception("该选项是已选中状态：%s" % option.text)

    def _unsetSelected(self, option):
        """
        将已选选项置为未选状态（仅限于三级选项）
        :param option:
        :return:
        """
        check_ele = option.find_element_by_xpath('./span[2]')
        if check_ele.get_attribute('class') == 'button chk checkbox_true_full':
            check_ele.click()
        else:
            raise Exception("该选项是未选中状态：%s" % option.text)

    def get_options(self):
        """
        获取下拉中的所有选项
        备注：对于接触网缺陷，由于页面不能完整展示，所以不能获取到完整的缺陷列表，后期优化
        :return: 按字典方式返回
        """
        logger.info("获取所有的缺陷类型")
        values = dict()
        self._text_el.click()
        groups = self._dr.find_elements_by_css_selector('#' + self._sid + ' > li > ul > li')

        for gp in groups:
            time.sleep(1)
            title = gp.text
            values[title] = []
            gp.find_element_by_xpath('./span[1]').click()
            time.sleep(1)
            lists = gp.find_elements_by_xpath('./ul/li')
            for list in lists:
                values[title].append(list.text)
            time.sleep(1)
            gp.find_element_by_xpath('./span[1]').click()
        time.sleep(1)
        self._text_el.click()
        logger.info("缺陷类型的值为：")
        logger.info(values)
        return values

    def deselect_all(self):
        """
        通过缺陷类型的复选框按钮，取消所有选项
        :return:
        """
        # 找到缺陷类型复选框，并判断button状态
        time.sleep(2)
        self._text_el.click()
        defect_check = self._dr.find_element_by_xpath('//*[@id="' + self._sid + '"]/li/span[2]')
        if defect_check.get_attribute('class') == 'button chk checkbox_false_part':   # 连续点击两次实现取消
            defect_check.click()
            defect_check.click()
        elif defect_check.get_attribute('class') == 'button chk checkbox_false_full':   # 如果已经是全部取消状态，则给出提示
                logger.warning('缺陷类型已经是全部取消状态')
        else:
            defect_check.click()
        self._text_el.click()

    def select_all(self):
            """
            通过缺陷类型的复选框按钮，选中所有选项
            button的四种状态：button chk checkbox_true_part(选中但不是全选)
                              button chk checkbox_true_full（选中且全选）
    	                      button chk checkbox_false_full（未选中，下级菜单也无选中）
    	                      button chk checkbox_false_part（未选中，但下级菜单部分选中）
            :return:
            """
            # 找到缺陷类型复选框，并判断button状态'//*[@id="' + self._sid + '"]/div[1]/input'
            self._text_el.click()
            defect_check = self._dr.find_element_by_xpath('//*[@id="' + self._sid + '"]/li/span[2]')
            if defect_check.get_attribute('class') == 'button chk checkbox_true_part':  # 如果是部分选中，连续点击两次即实现全选
                defect_check.click()
                defect_check.click()
            elif defect_check.get_attribute('class') == 'button chk checkbox_true_full':  # 如果已经是全选状态，则给出提示
                logger.warning('缺陷类型已经是全选状态')
            else:
                defect_check.click()
            self._text_el.click()

    def select_by_text(self, Dict):
        """
        根据text选择选项
        :param Dict: 字典{'弓网缺陷':['疑似燃弧', '疑似定位线夹燃弧']，'接触网缺陷':['接触线硬弯', '疑似绝缘器消弧缺失']}   如果列表为空[]，表示全选
        :return:set_option[] 成功设置的选项
        """
        set_option = []
        Keys = Dict.keys()
        time.sleep(1)
        self._text_el.click()
        time.sleep(1)
        groups = self._dr.find_elements_by_css_selector('#' + self._sid + ' > li > ul > li')
        for key in Keys:
            for gp in groups:
                if key == gp.text:
                    time.sleep(1)
                    gp.find_element_by_xpath('./span[1]').click()
                    time.sleep(1)
                    if len(Dict.get(key)) == 0:
                        key_value = []
                        for option in gp.find_elements_by_xpath('./ul/li'):
                            key_value.append(option.text)
                        Dict[key] = key_value
                    for value in Dict.get(key):
                        for option in gp.find_elements_by_xpath('./ul/li'):
                            if value == option.text:
                                self._setSelected(option)
                                set_option.append(option.text)
                                time.sleep(1)
                                break
                    time.sleep(1)
                    gp.find_element_by_xpath('./span[1]').click()
                    break
        self._text_el.click()
        logger.info("成功设置的选项为：")
        logger.info(set_option)
        return set_option

    def deselect_by_text(self, Dict):
        """
        根据text取消选项
        :param Dict: 字典{'弓网缺陷':['疑似燃弧', '疑似定位线夹燃弧']，'接触网缺陷':['接触线硬弯', '疑似绝缘器消弧缺失']}   如果列表为空[]，表示全选
        :return:set_option[] 成功取消的选项
        """
        set_option = []
        Keys = Dict.keys()
        time.sleep(1)
        self._text_el.click()
        time.sleep(1)
        groups = self._dr.find_elements_by_css_selector('#' + self._sid + ' > li > ul > li')
        for key in Keys:
            for gp in groups:
                if key == gp.text:
                    time.sleep(1)
                    gp.find_element_by_xpath('./span[1]').click()
                    time.sleep(1)
                    if len(Dict.get(key)) == 0:
                        key_value = []
                        for option in gp.find_elements_by_xpath('./ul/li'):
                            key_value.append(option.text)
                        Dict[key] = key_value
                    for value in Dict.get(key):
                        for option in gp.find_elements_by_xpath('./ul/li'):
                            if value == option.text:
                                self._unsetSelected(option)
                                set_option.append(option.text)
                                time.sleep(1)
                                break
                    time.sleep(1)
                    gp.find_element_by_xpath('./span[1]').click()
                    break
        self._text_el.click()
        logger.info("成功设置的选项为：")
        logger.info(set_option)
        return set_option

    def input_key_search(self, keyword):
        """
        在搜索框输入关键字keyword（返回查询结果）
        :param keyword:
        :return:
        """
        logger.info("根据关键字，查询缺陷类型")
        values = dict()
        time.sleep(1)
        self._text_el.click()  # 点击文本框，弹出搜索框
        time.sleep(1)
        search_ele = self._dr.find_element_by_xpath('//*[@id="' + self._sid + '"]/preceding-sibling::div[1]/input')  # 找到搜索框
        time.sleep(1)
        search_ele.click()  # 点击搜索框
        time.sleep(1)
        search_ele.clear()
        search_ele.send_keys(keyword)  # 输入搜索关键字
        time.sleep(1)
        groups = self._dr.find_elements_by_css_selector('#' + self._sid + ' > li > ul > li')

        for gp in groups:
            time.sleep(1)
            title = gp.find_element_by_xpath('./a').text
            if title.strip() == '':          # 如果二级菜单隐藏，则进入下一次循环
                continue
            values[title] = []
            time.sleep(1)
            lists = gp.find_elements_by_xpath('./ul/li')
            for list in lists:
                if list.get_attribute('style') != 'display: none;':      # 如果缺陷类型不是隐藏，则保存其值
                    values[title].append(list.text)
            time.sleep(1)
        logger.info("查询到的缺陷类型为：")
        logger.info(values)
        return values

    def select_key_search_text(self, keyword, Dict):
        """
        在搜索框输入关键字：keyword，然后通过字典选择对应的选项（同select_by_text）
        :param keyword:
        :param Dict:
        :return:
        """
        logger.info('在搜索框中输入关键字, 并根据字典选择对应选项')
        # search_options = self.input_key_search(keyword)
        time.sleep(1)
        self._text_el.click()  # 点击文本框，弹出搜索框
        time.sleep(1)
        search_ele = self._dr.find_element_by_xpath('//*[@id="' + self._sid + '"]/preceding-sibling::div[1]/input')  # 找到搜索框
        time.sleep(1)
        search_ele.click()  # 点击搜索框
        time.sleep(1)
        search_ele.clear()
        search_ele.send_keys(keyword)  # 输入搜索关键字
        time.sleep(1)
        groups = self._dr.find_elements_by_css_selector('#' + self._sid + ' > li > ul > li')
        set_option = []  # 保存所设置的选项
        Keys = Dict.keys()

        for key in Keys:
            for gp in groups:
                if key == gp.find_element_by_xpath('./a').text:
                    time.sleep(1)
                    #so.find_element_by_xpath('./span[1]').click()
                    #time.sleep(1)
                    if len(Dict.get(key)) == 0:              # 如果传入的参数，列表为空，则将列表的值置为所有选项
                        key_value = []
                        for option in gp.find_elements_by_xpath('./ul/li'):
                            if option.get_attribute('style') != 'display: none;':
                                key_value.append(option.text)
                        Dict[key] = key_value
                    for value in Dict.get(key):
                        for option in gp.find_elements_by_xpath('./ul/li'):
                            if value == option.text:
                                self._setSelected(option)
                                set_option.append(option.text)
                                time.sleep(1)
                                break
                    time.sleep(1)
                    # gp.find_element_by_xpath('./span[1]').click()
                    break
        self._text_el.click()
        logger.info("成功设置的选项为：")
        logger.info(set_option)
        return set_option

    def clear_button_text(self):
        """
        清除文本框中的所有信息，
        :return:无返回值
        """
        logger.info("清除文本框中的所有信息")
        self._dr.find_element_by_xpath('//*[@id="' + self._id + '"]/following-sibling::a').click()

    def clear_button_search(self):
        """
        清除搜索框中的所有信息，
        前置条件，进入了查询区域或者输入了查询信息
        :return:无返回值
        """
        logger.info("清除搜索框中的所有信息")
        time.sleep(1)
        self._text_el.click()
        time.sleep(1)
        self._dr.find_element_by_xpath('//*[@id="' + self._sid + '"]/preceding-sibling::div/a').click()

# 状态选择（同点对比）
class StatusSelector(BaseSelector):
    """        应用范围：状态选择（同点对比）
    该复选框与其他不同，文本框没有id，目前处理办法是根据文本框css名，关联列表
     """
    def __init__(self, driver, css):
        # 该判断不太合理，需要进一步研究
        self._dr = driver
        self._css = css
        BaseSelector.__init__(self, self._text_el, self._options_el)

    @property
    def _options_el(self):
        # self._text_el.click()
        # 通过选择输入框的ＩＤ关联选项区域并找到选项区域ＩＤ
        self._scss = dict_relate_id[self._css]
        options = self._dr.find_element_by_css_selector(self._scss).find_elements_by_xpath('./ul/li')
        # self._text_el.click()
        return options

    @property
    def _text_el(self):
        return driver.find_element_by_css_selector(self._css)      # 定位文本框

    def select_all(self):
        """
        全选按钮
        :return:
        """
        time.sleep(1)
        self._text_el.click()     # 点击文本框，弹出下拉列表
        time.sleep(1)
        select_all_button = self._dr.find_element_by_css_selector(self._scss).find_element_by_xpath('./div/ul/li[1]/a')   # 定位全选按钮
        select_all_button.click()
        time.sleep(1)
        self._text_el.click()     # 收起下拉列表

    def deselect_all(self):
        """
        全不选按钮
        :return:
        """
        time.sleep(1)
        self._text_el.click()     # 点击文本框，弹出下拉列表
        time.sleep(1)
        select_all_button = self._dr.find_element_by_css_selector(self._scss).find_element_by_xpath('./div/ul/li[2]/a')   # 定位全不选按钮
        select_all_button.click()
        time.sleep(1)
        self._text_el.click()     # 收起下拉列表

    def close_button(self):
        """
        关闭按钮（前提：下拉列表弹出）
        :return:
        """
        time.sleep(1)
        select_all_button = self._dr.find_element_by_css_selector(self._scss).find_element_by_xpath('./div/ul/li[3]')  # 定位关闭按钮
        select_all_button.click()

    def _setSelected(self, option):
        """
        将未选选项置为选择状态
        :param option:
        :return:
        """
        time.sleep(1)
        check_ele = option.find_element_by_xpath('./label/input')      # 找到对应复选框
        print(check_ele.get_attribute('checked'))
        if check_ele.get_attribute('checked') != 'true':     # 如果复选框时未选择状态，则点击，否则抛出异常
            check_ele.click()
        else:
            raise Exception("该选项是已选中状态：%s" % option.text)

    def _unsetSelected(self, option):
        """
        将已选选项置为未选状态
        :param option:
        :return:
        """
        check_ele = option.find_element_by_xpath('./label/input')
        if check_ele.get_attribute('checked') == 'true':
            check_ele.click()
        else:
            raise Exception("该选项是未选中状态：%s" % option.text)

    def select_by_text_list(self, textlist):
        """
        选择下拉列表（根据text（下拉列表的文字）选择）-------参数为list
        :param textlist:   ['新上报', '已取消', '已确认']
        :return:opTextList  所选择的选项
        """
        logger.info("通过选项文本设置选项")
        time.sleep(1)
        self._text_el.click()
        time.sleep(1)
        opTextList = []
        for text in textlist:
            matched = False
            for opt in self._options:
                opText = opt.text.strip()
                if opText == text.strip():
                    self._setSelected(opt)
                    opTextList.append(opText)
                    matched = True
                    break
            if not matched:
                raise NoSuchElementException("Cannot locate option with value: %s" % text)
        logger.info("所选择的选项为：")
        logger.info(opTextList)
        self._text_el.click()  # 收起下拉列表
        return opTextList


    def deselect_by_text_list(self, textlist):
        """
        选择下拉列表（根据text（下拉列表的文字）取消选择）-------参数为list
        :param textlist:   ['新上报', '已取消', '已确认']
        :return:opTextList  所取消的选项
        """
        logger.info("通过选项文本设置选项（取消已选选项）")
        time.sleep(1)
        self._text_el.click()
        time.sleep(1)
        opTextList = []
        for text in textlist:
            matched = False
            for opt in self._options:
                opText = opt.text.strip()
                if opText == text.strip():
                    self._unsetSelected(opt)
                    opTextList.append(opText)
                    matched = True
                    break
            if not matched:
                raise NoSuchElementException("Cannot locate option with value: %s" % text)
        logger.info("所取消的选项为：")
        logger.info(opTextList)
        self._text_el.click()  # 收起下拉列表
        return opTextList

    def get_value(self):
        '''
        获取当前输入框中的值
        :return: 当前输入框中的值
        '''
        logger.info("获取当前选择框中的值")
        logger.info("当前选择框中的值为：" + self._el.text)
        return self._el.text

# 主动检测入口（）
class OriginalFileSelector(object):
    def __init__(self, driver):
        self._id = 'OriginalFile'
        self._dr = driver

    def mouse_moves_to(self):
        """
        鼠标移动到入口按钮处，并判断是否展示下拉列表
        :return:
        """
        element = self._dr.find_element_by_css_selector('#' + self._id)   # 找到缺陷详情页的入口按钮
        ActionChains(self._dr).move_to_element(element).perform()       # 鼠标移动到入口按钮处
        # 判断是否显示列表
        ele_list = self._dr.find_element_by_css_selector('#' + self._id).find_element_by_xpath('./span[3]')
        if ele_list.get_attribute('style') == 'display: none;':
            return True
        else:
            logger.error("操作有误，原始数据列表没有显示")
            return False

    def get_originalfile(self):
        """点击选项：主动获取原始数据"""
        self.mouse_moves_to()
        entrance_originalfile = self._dr.find_element_by_css_selector('#' + self._id).find_element_by_xpath('./span[2]')
        entrance_originalfile.click()

    def new_originalfile(self):
        """点击选项：新建原始数据获取
        :return:
        """
        self.mouse_moves_to()
        entrance_originalfile = self._dr.find_element_by_css_selector('#' + self._id).find_element_by_xpath('./span[3]')
        entrance_originalfile.click()



if __name__ == "__main__":
    # url1 = 'http://183.203.132.154:9100'
    url1 = 'http://183.129.132.155:10001/C3/index_3C_new.html?userName=admin&v=DPC_3C_5.0.3.035'
    # url1 = 'http://183.203.132.154:9100/C3/PC/MAlarmMonitoring/MonitorAlarm3CForm4.htm?alarmid=F23dcab41450047f2b8c88be58e695a22'
    url = 'http://183.129.132.155:10001/C3/PC/MAlarmMonitoring/MonitorAlarm3CForm4.htm?alarmid=Fb59290bff65a46c1b829921a49584e60&example-basic=%E4%B8%80%E7%B1%BB&example-basic=%E4%BA%8C%E7%B1%BB&ddlzt=AFSTATUS01&ddlzt=AFSTATUS03&ddlzt=AFSTATUS04&ddlzt=AFSTATUS05&saved_ids=&juselect=0&duanselect=0&carType=0&IsAbnormity=&direction=&txtpole=&txt_fx=&JXWJ=0&IsLock=0&ztree=&START_NUM_PIXELS=&END_NUM_PIXELS=&txt_temp_hw1=&txt_temp_hw2=&txt_temp_hj1=&txt_temp_hj2=&txt_bow=0&txt_dg1=&txt_dg2=&txt_lc1=&txt_lc2=&txt_speed1=&txt_speed2=&ju=0&duanText=%u5168%u90E8&jwd=0&jb=%E4%B8%80%E7%B1%BB%E4%BA%8C%E7%B1%BB&jlh=&locid=&startdate=2018-08-15%2000:00:00&enddate=2018-08-16%2023:59:59&zt=AFSTATUS01AFSTATUS03AFSTATUS04AFSTATUS05&orgCode=0&orgName=&orgType=&locationCode=undefined&locationName=&locationType=undefined&startkm=&endkm=&afcode=&bjbm=&QX_mark=undefined&INITIAL_CODE=&INITIAL_CODE_TYPE=&REPORT_PERSON=&SCENCESAMPLE_STR=&VI_ANALYSIS=&OX_ANALYSIS=&xb=0&code=&code_type=&qz=undefined&show_repeat=&bug_switch=&position_null=&weekly=&JC_TYPE=&start_report_date=&end_report_date=&start_per_of_arc=&end_per_of_arc=&StatisticsSign=&ACFLAG_CODE=&SAMPLE_CODE=&SAMPLE_TYPE=&ISCLOCK=0&IS_TRANS_ALLOWED=&is_spark=&criterion=&notIncludedRepeatHistory=&RepeatdivceType=&alarm_order_sign=&RepeatdivceType=&IsAbnormity=&data_type=SUPERVISE&v=DPC_3C_5.0.3.035'
    # driver=CreateDriver.getBrowserDriver()
    driver = webdriver.Chrome()
    #print(driver)
    driver.maximize_window()
    driver.get(url1)
    driver.find_element_by_id('username').send_keys('admin')
    driver.find_element_by_id('password').send_keys('cdgt@qwer')
    driver.find_element_by_class_name("login_go").click()
    driver.get(url)
    time.sleep(3)

    #<AlarmTypeSelector>测试脚本1（？？？？？？？）---报警类型选择
    # 进入一个缺陷详情页面，点击确认按钮

    '''
    driver.find_element_by_id('E_btnOk2').click()
    time.sleep(3)
    driver.switch_to.frame('iframe_AlarmSure')
    alarm = AlarmTypeSelector(driver, 'citySel')
    time.sleep(2)
    print("测试alarm.get_options()")
    print(alarm.get_options())
    #print(alarm.getAllValue())
    time.sleep(2)
    # print(alarm.get_Value())
    # print(alarm.getValue())
    time.sleep(2)
    print(alarm.input_message("疑似线夹燃弧"))
    time.sleep(2)
    print(alarm.select_by_code("FXYSGJYQLF"))
    time.sleep(2)
    print(alarm.select_by_order(5))
    time.sleep(2)
    print(alarm.select_by_text("疑似跨中接触线燃弧"))
    '''


    # <AlarmCurveSelector>测试脚本2---报警曲线选择

    '''webElement = driver.find_element_by_id('divDropButton')
    se = AlarmCurveSelector(webElement)
    print('------------select_by_visible_text("温度曲线")-----------------')
    se.select_by_visible_text('温度曲线')
    print(se.get_value())
    time.sleep(1)
    print('------------select_by_visible_text("拉出值曲线")-----------------')
    se.select_by_visible_text('拉出值曲线')
    print(se.get_value())
    time.sleep(1)
    print('------------select_by_index(-1)-----------------')
    print(se.select_by_index(-1))
    print(se.get_value())
    time.sleep(1)
    print('------------select_by_index(10)-----------------')
    print(se.select_by_order(10))
    print(se.get_value())
    time.sleep(1)
    print('------------select_by_index(2)-----------------')
    print(se.select_by_order(2))
    print(se.get_value())
    print("OK")
    time.sleep(1)
    print(se.get_options())'''

    #<OptionSelector>测试脚本3---报警级别选择
    '''
    driver.find_element_by_id('E_btnOk2').click()
    time.sleep(3)
    driver.switch_to.frame('iframe_AlarmSure')
    print("修改之前的值：", OptionSelector(driver.find_element_by_id('Useverity')).getValue())
    time.sleep(2)
    #print(OptionSelector(driver.find_element_by_id('Useverity')).all_selected_options)
    #print(OptionSelector(driver.find_element_by_id('Useverity')).first_selected_option)
    #print(OptionSelector(driver.find_element_by_id('Useverity')).options)
    OptionSelector(driver.find_element_by_id('Useverity')).select_by_visible_text('一级')
    time.sleep(2)
    print("修改之后的值：",OptionSelector(driver.find_element_by_id('Useverity')).getValue())
    time.sleep(2)
    #time.sleep(2)
    print("全部选项：",OptionSelector(driver.find_element_by_id('Useverity')).getAllOption())
    '''

    # <ExportSelector>测试脚本4----导出
    '''
    time.sleep(3)
    exp = ExportSelector(driver.find_element_by_xpath('//*[@id="btns_all"]/div[4]'))
    print(driver.find_element_by_xpath('//*[@id="btns_all"]/div[4]').get_attribute('class'))
    print(exp.get_options())
    print(exp.get_value())
    #print("exp.select_by_visible_text('重新生成缺陷报告')")
    #print(exp.select_by_visible_text('重新生成缺陷报告'))
    #print("End")
    print(exp.select_by_order(2))
    '''

    # <AlarmDealSelector>测试脚本5----报警分析
    # 进入一个缺陷详情页面，点击确认按钮

    '''
    time.sleep(3)
    driver.find_element_by_id('E_btnOk2').click()
    time.sleep(2)
    driver.switch_to.frame('iframe_AlarmSure')
    alarmdeal = AlarmDealSelector(driver, 'UtxtDefect')
    print("测试alarmdeal.get_value()")
    print(alarmdeal.get_value())
    print("测试alarmdeal.get_options()")
    print(alarmdeal.get_options())
    # print("测试select_by_order")
    # print(alarmdeal.select_by_order(3))
    # print("测试select_by_visible_text")
    # print(alarmdeal.select_by_visible_text("接触线硬弯"))
    #alarmdeal.clearSelector()
    print("测试select_key_search_order")
    print(alarmdeal.select_key_search_order('线', 2))
    print("测试input_key_search_text")
    print(alarmdeal.input_key_search_text('线', '线夹打弓'))
    # time.sleep(2)
    # alarmdeal.input_message_text("测试", mode='a')
    # time.sleep(3)
    # alarmdeal.clear()
    # time.sleep(3)
    '''

    # <AlarmDealSelector>测试脚本6----处理建议
    # 进入一个缺陷详情页面，点击确认按钮

    '''
    time.sleep(3)
    driver.find_element_by_id('E_btnOk2').click()
    time.sleep(2)
    driver.switch_to.frame('iframe_AlarmSure')
    dealadvice = AlarmDealSelector(driver, 'UtxtAdvice')
    # print("dealadvice.get_value()")
    # print(dealadvice.get_value())
    # print("测试dealadvice.get_options()")
    # print(dealadvice.get_options())
    print("测试select_by_order")
    print(dealadvice.select_by_order(1))
    print("测试select_by_visible_text")
    print(dealadvice.select_by_visible_text("天窗检修"))
    print("测试select_key_search_order")
    print(dealadvice.select_key_search_order('停电车巡', 2))
    dealadvice.clearSelector()
    print("测试input_key_search_text")
    print(dealadvice.input_key_search_text('天', '天窗检修'))
    '''

    # <DefectMarkSelector>测试脚本7----缺陷标记
    # 进入一个缺陷详情页面，点击确认按钮
    '''
    time.sleep(3)
    driver.find_element_by_id('E_btnOk2').click()
    time.sleep(2)
    driver.switch_to.frame('iframe_AlarmSure')
    defectmark = DefectMarkSelector(driver, 'DefectMark')
    defectmark.get_options()
    # defectmark.select_by_order(2)
    defectmark.get_value()
    #defectmark.select_by_visible_text('局部和全景补光不足')
    #defectmark.select_by_order([5, 8, 2, 3])
    #defectmark.deselect_by_order_list([2, 3, 8, 5])
    #defectmark.select_by_text_list(['火花小', '局部曝光过度', '全景曝光过度', '雨天红外成像效果差', '隧道红外成像效果差', '局部成像效果差'])
    #defectmark.deselect_by_text_list(['火花小', '局部曝光过度', '全景曝光过度', '雨天红外成像效果差', '隧道红外成像效果差', '局部成像效果差'])
    defectmark.select_by_text(['火花小', '局部曝光过度', '全景曝光过度', '雨天红外成像效果差', '隧道红外成像效果差', '局部成像效果差'])
    defectmark.get_value()
    #defectmark.get_allselected()
    #defectmark.deselect_all()
    #defectmark.clear_button_text()
    #defectmark.select_key_search_order("条纹", [1, 2, 3])
    defectmark.select_key_search_text('条纹', ['局部横条纹', '局部竖条纹', '全景横条纹', '全景竖条纹'])

    #defectmark.select_by_order(1)
    #defectmark.select_by_order(2)
    '''

    # <SceneSampleSelector>测试脚本8----场景样本
    '''
    confirm_button = (By.ID, 'E_btnOk2')
    WebDriverWait(driver, 10, 0.5).until(EC.presence_of_element_located(confirm_button))
    driver.find_element_by_id('E_btnOk2').click()
    time.sleep(1)
    driver.switch_to.frame('iframe_AlarmSure')
    scenesample = SceneSampleSelector(driver, 'SceneSample_Sure')
    #scenesample.select_by_order([1, 3, 5, 7])
    scenesample.select_by_text(['换线', '折线下半截短', '高弓多线', '普通画质好多线'])
    scenesample.get_allselected()
    #scenesample.deselect_by_order_list([1, 3, 5, 7])
    #scenesample.deselect_by_text_list(['换线', '折线下半截短', '高弓多线', '普通画质好多线'])
    scenesample.deselect_all()
    scenesample.input_key_search('线')
    #scenesample.select_key_search_order('线', [1, 2, 3, 4])
    #scenesample.select_key_search_text('线', ['换线', '折线下半截短', '高弓多线', '普通画质好多线'])
    #scenesample.clear_button()
    scenesample.shutdown_button()
    '''

    # <TimeSelector>测试脚本8----时间控件
    '''
    confirm_button = (By.ID, 'E_btnOk2')
    WebDriverWait(driver, 10, 0.5).until(EC.presence_of_element_located(confirm_button))
    driver.find_element_by_id('E_btnOk2').click()
    time.sleep(1)
    driver.switch_to.frame('iframe_AlarmSure')
    timeselect = TimeSelector(driver, 'Ureportdate')
    timeselect.settime('2018-07-16 12:36:02')
    #timeselect.settime('test')
    text = timeselect.catch_alert()
    print(text)
    '''

    # <DefectTypesSelector>测试脚本9----缺陷类型（同点对比）
    '''
    TongDianDuiBi = (By.XPATH, '//*[@id="TOP_three"]/div[1]/div[2]/ul/li[6]/button')
    WebDriverWait(driver, 10, 0.5).until(EC.presence_of_element_located(TongDianDuiBi))
    driver.find_element_by_xpath('//*[@id="TOP_three"]/div[1]/div[2]/ul/li[6]/button').click()
    time.sleep(1)
    defecttype = DefectTypesSelector(driver, 'citySel')
    #defecttype.get_options()
    #print(defecttype.get_options())
    #defecttype.select_all()
    defecttype.deselect_all()
    #defecttype.select_by_text({'弓网缺陷': ['疑似燃弧', '疑似定位线夹燃弧'], '接触网缺陷': ['接触线硬弯', '疑似绝缘器消弧缺失']})
    #defecttype.deselect_by_text({'弓网缺陷': ['疑似燃弧', '疑似定位线夹燃弧'], '接触网缺陷': ['接触线硬弯', '疑似绝缘器消弧缺失']})
    #defecttype.deselect_by_text({'弓网缺陷': [], '受电弓缺陷': []})
    #defecttype.input_key_search('线')
    defecttype.select_key_search_text('弧', {'弓网缺陷': ['疑似燃弧', '疑似定位线夹燃弧'], '接触网缺陷': ['疑似绝缘器消弧缺失']})
    # defecttype.clear_button_text()
    defecttype.clear_button_search()
    '''

    # <StatusSelector>测试脚本10----状态选择（同点对比）
    '''
    TongDianDuiBi = (By.XPATH, '//*[@id="TOP_three"]/div[1]/div[2]/ul/li[6]/button')
    WebDriverWait(driver, 10, 0.5).until(EC.presence_of_element_located(TongDianDuiBi))
    driver.find_element_by_xpath('//*[@id="TOP_three"]/div[1]/div[2]/ul/li[6]/button').click()
    time.sleep(1)
    status = StatusSelector(driver, 'button.ui-multiselect.ui-widget.ui-state-default.ui-corner-all')
    #status.select_all()
    status.deselect_all()
    #status.close_button()
    #status.deselect_by_text_list(['新上报', '已取消', '已确认', '检修中'])
    status.select_by_text_list(['新上报', '已取消', '已确认', '检修中'])
    print("目前设置的值为：")
    print(status.get_value())
    '''

    # <OriginalFileSelector>测试脚本11----主动检测
    OriginalFile = OriginalFileSelector(driver)
    #OriginalFile.get_originalfile()
    OriginalFile.new_originalfile()

    # 测试is_displayed
    '''
    time.sleep(3)
    driver.find_element_by_id('E_btnOk2').click()
    time.sleep(2)
    driver.switch_to.frame('iframe_AlarmSure')
    element1 = driver.find_element_by_xpath('//*[@id="UtxtAdvice"]')
    element1.click()
    element2 = driver.find_element_by_xpath('//*[@id="ULUtxtAdvice"]')
    # element2 = driver.find_element_by_xpath('//*[@id="ULUtxtAdvice_2"]')
    #element2 = driver.find_element_by_xpath('//*[@id="ULUtxtAdvice_2_a"]')
    # element2 = driver.find_element_by_xpath('//*[@id="ULUtxtAdvice_2_span"]')
    # element2.is_displayed()
    print(element2.is_displayed())
    if element2.is_displayed():
        print("可见")
    else:
        print("不可见")
    '''

    wait = input("输入任意字符退出：")
    driver.close()
