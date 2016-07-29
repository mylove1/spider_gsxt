# -*- coding:utf-8 -*-
import re
import sys
import traceback
import threading

reload(sys)
sys.setdefaultencoding('utf-8')

PHANTOMJSDIRPATH = 'D:\\python\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe'
#PHANTOMJSDIRPATH = 'C:\\Python27\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe'

class Tool:
    def __init__(self):
        pass

    def getRuleString(self, diver, url, rule):
        try:
            diver.get(url)
            response = diver.page_source.encode('utf-8')
            pattern = re.compile(rule)
            items = re.findall(pattern,response)
            return items
        except Exception,e:
            print traceback.print_exc()

    def getRulePageStringMul(self, page, rule):
        try:
            pattern = re.compile(rule)
            items = re.findall(pattern, page)
            return items
        except Exception,e:
            print traceback.print_exc()

    def getRulePageStringOne(self, page, rule):
        try:
            pattern = re.compile(rule)
            if re.search(pattern, page) != None:
                return re.search(pattern, page).group(1)
            else:
                return None
        except Exception,e:
            print traceback.print_exc()

    def has_page_load(self, driver):
        return driver.execute_script("return document.readyState") == 'complete'

