# -*- coding:utf-8 -*-
import sys
import re
import threading
import time
import string
import traceback
from selenium import webdriver

reload(sys)
sys.setdefaultencoding('utf-8')

sys.path.append("E:\python_proj")
from lib.config import *

class ZheJiang:
    def __init__(self, url):
        self.url = url
        self.tool = Tool()
        self.pageNum = 0
        self.pageNumAll = 0
        self.browser = webdriver.PhantomJS(executable_path = PHANTOMJSDIRPATH )

    def close(self):
        return self.browser.quit()

    def InputExceptionListPage(self):
        rule = '(经营异常名录)\s*\$.*?action.*?\"(.*?)\"'
        items = self.tool.getRuleString(self.browser, self.url, rule)
        pass
