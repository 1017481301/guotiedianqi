from selenium import webdriver
from abc import ABCMeta,abstractmethod,ABC
from selenium.common.exceptions import NoSuchElementException, UnexpectedTagNameException
from log.TestLogBook import run_log as logger
import time

# 对下拉控件的操作和信息提取封装了一个基础类
class BaseSelector(ABC):
    __metaclass__ = ABCMeta
    def __init__(self,webElement,optionElements):

        #判定driver是否正常
        '''
        if (type(webElement) is not webdriver.chrome.webdriver.WebDriver):
            message='{}\'s type error,must be "webdriver.chrome.webdriver.WebDriver"'.format(webElement)
            logger.info(message)
            raise UnexpectedTagNameException(message)
        '''
        self._el = webElement
        self._options = optionElements


    @abstractmethod
    def _options_el(self):
        '''please Implemente in subclass'''

    @abstractmethod
    def _text_el(self):
        '''please Implemente in subclass'''

    def get_value(self):
        '''
        获取当前输入框中的值
        :return: 当前输入框中的值
        '''
        logger.info("获取当前选择框中的值")
        logger.info("当前选择框中的值为：" + self._el.get_attribute('value'))
        return self._el.get_attribute('value')

    def get_now_option(self):
        logger.info("获取当前被选中的下拉项")

    def get_options(self):
        self._el.click()
        time.sleep(1)
        logger.info("获取所有选项：")
        values=[]
        for opt in self._options:
            if ''==opt.text:
                continue
            values.append(opt.text.strip())
        self._el.click()
        logger.info(values)
        return values

    def select_by_code(self, code):
        logger.info("通过页面code=" + code + "属性设置选项")  # 部分下拉列表没有code属性
        self._el.click()
        time.sleep(1)
        matched = False
        for opt in self._options:
            opCode = opt.get_attribute('code')
            opText = opt.text
            #print(opCode,code)
            if opCode.strip() == code.strip():
                opt.click()
                matched=True
                logger.info("所设置的选项为：" + opText)
                return opText
        if not matched:
            raise NoSuchElementException("Cannot locate option with value: %s" % code)

    def select_by_index(self, code):
        logger.info("通过元素index属性设置选项")

    def select_by_order(self, order):
        """
        通过下拉选项从上致下的顺序选择相应的值
        :param index:选择1致选项总数
        :return:返回选择的值
        """
        logger.info("通过元素在HTML中的顺序设置选项")
        time.sleep(1)
        self._el.click()
        time.sleep(1)
        n=1
        if len(self._options)<order:
            order=len(self._options)
            logger.warning("输入order大于选项总数，将order置为选项总数")
        if order<1:
            order=1
            logger.warning("输入order小于1，将order置为1")
        for opt in self._options:
            if n == order:
                opText = opt.text
                opt.click()
                logger.info("所设置的选项为：" + opText)
                return opText
            n = n + 1

    def select_by_visible_text(self, text):
        """
            Deselect all a that have a value matching the argument. That is, when given "温度曲线" this would deselect an option like:
                <a id="wd" href="javascript:void(0);" style="color: White;">温度曲线</a>
                    :Args:
                        - value - The value to match against
            throws NoSuchElementException If there is no option with specisied value in SELECT
        """
        logger.info("通过选项文本设置选项")
        time.sleep(1)
        self._el.click()
        time.sleep(1)
        matched=False
        for opt in self._options:
            opText=opt.text.strip()
            #print(opText,text)
            if opText == text.strip():
                opt.click()
                matched=True
                logger.info("所设置的选项为：" + opText)
                return opText
        if not matched:
            raise NoSuchElementException("Cannot locate option with value: %s" % text)

    def get_button_hint(self):
        logger.info("返回title"+ self._el.title)
        return self._el.title
if __name__=="__main__":
    BaseSelector(1).select_by_id('22')