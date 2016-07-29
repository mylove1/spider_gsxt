# -*- coding:utf-8 -*-
import sys
import re
import threading
import time
import string
import traceback
import bsddb
from selenium import webdriver
from config import *

reload(sys)
sys.setdefaultencoding('utf-8')

areaDic = {'青海':'QinHai', '辽宁':'LiaoNing', '贵州':'GuiZhou', '北京':'BeiJin', '国家工商行政管理总局':'ZongJu', '广西':'GuangXi', '广东':'GuangDong', '上海':'ShangHai',
'海南':'HaiNan', '甘肃':'GanSu', '山东':'ShanDong' , '江西':'JiangXi', '宁夏':'NingXia', '湖南':'HuNan', '河北':'HeBei', '西藏':'XiZang', '吉林':'JiLin', '黑龙江':'HeiLongJiang' ,
'福建':'FuJiang', '天津':'TianJin', '内蒙古':'NeiMengGu', '安徽':'AnHui', '陕西':'ShanXi', '山西':'Shan1Xi', '新疆':'XinJiang', '四川':'SiChuan', '重庆':'ChongQing', '湖北':'HuBei',
'江苏':'JiangSu', '河南':'HeNan', '浙江':'ZheJiang', '云南':'YunNan'}

class GSXTIndex:
    def __init__(self, url):
        self.tool = Tool()
        self.url = url
        self.browser = webdriver.PhantomJS(executable_path=PHANTOMJSDIRPATH)

    def start(self):
        try:
            rule = '_trackEvent.*?>(.*?)<'
            items = self.tool.getRuleString(self.browser, self.url, rule)
            urlcarry = {}
            for item in items:
                hrefstring = self.browser.find_element_by_link_text(item).get_attribute('href')
                urlcarry[areaDic[item]] = hrefstring
            return urlcarry
        except Exception, e:
            print traceback.print_exc()
        self.close()
    def close(self):
        return self.browser.quit()

if __name__ == "__main__":
    url = 'http://gsxt.saic.gov.cn/'

    spider = GSXTIndex(url)
    urlCarry = spider.start()
    for item in urlCarry:
        print item
        #print urlCarry[item]

