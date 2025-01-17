__author__ = 'liangzhong'
'''
功能介绍：
    本模块主要完成对各个部件进行封装，提供给页面层和业务流程调用，实现对控件的高复用。
    控件：单/多行文本框、时间控件、下拉控件、查询树、选择树、单/复选框、文件上传/下载、系统自定义控件等
    表单：表单填写、表单信息获取、查询等
    提供以上封装控件的所有炒作操作方法、信息获取方法、结果反馈等
----------------------------------------------------------------------------------------------------------
编程理念：
        Web系统都是由高复用的各个控件组合完成增、删、改、查、分析等工作，而这些控件本身存在高度的可复用性，
    因此通过封装控件、列表，然后由上层封装或者测试用例调用该控件。
-----------------------------------------------------------------------------------------------------------
目前需要优化点：
    1.提取控件封装过程中的公共区域，形成公用方法
    2.加强异常处理
    3.接口说明及编程规范，接口提供规范的输出
    4.支持多线程
'''