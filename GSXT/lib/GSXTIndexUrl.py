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

class GSXTIndex:
    def __init__(self):
        self.tool = Tool()
        self.browser = webdriver.PhantomJS(executable_path=PHANTOMJSDIRPATH)

    def start(self, url):
        try:
            rule = '_trackEvent.*?>(.*?)<'
            items = self.tool.getRuleString(self.browser, url, rule)
            urlcarry = {}
            for item in items:
                hrefstring = self.browser.find_element_by_link_text(item).get_attribute('href')
                urlcarry[item] = hrefstring
            return urlcarry
        except Exception, e:
            print traceback.print_exc()

    def close(self):
        return self.browser.quit()

if __name__ == "__main__":
    url = 'http://gsxt.saic.gov.cn/'

    spider = GSXTIndex()
    urlCarry = spider.start(url)
    for item in urlCarry:
        print item
        #print urlCarry[item]
    spider.close()
