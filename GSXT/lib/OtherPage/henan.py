# -*- coding:utf-8 -*-
import sys
import re
import threading
import time
import string
import traceback
from selenium import webdriver


WORKDIRPATH = 'D:\\work\\GSXT'
sys.path.append(WORKDIRPATH)
from lib.config import *
from lib.Rules.HeNanRules import HENAN

class HeNan:
    def __init__(self, url):
        self.url = url
        self.tool = Tool()
        self.pageNum = 0
        self.pageNumAll = 0
        self.first = 0
        self.end = 0
        self.newurl = ''
        self.lastdata = HENAN()
        self.classname = 'HENAN'
        self.browser = webdriver.PhantomJS(executable_path=PHANTOMJSDIRPATH)
        self.start()

    def InputExceptionListPage(self, ):
        rule = 'href=\"(.*?)\".*?>经营异常名录<'
        items = self.tool.getRuleString(self.browser, self.url, rule)
        self.newurl = 'http://222.143.24.157' + items[0]
        #print self.newurl

    def close(self):
        return self.browser.quit()

    def getPageNumAll(self, page):
        rule = "jumpPage\('(.*?)'\).*?>确定<"
        tmpNum = self.tool.getRulePageStringOne(page, rule)
        if tmpNum == None:
            self.pageNumAll = 1
        else:
            self.pageNumAll = tmpNum

    def getPageNum(self, page):
        if self.end == 1:
            return self.pageNumAll
        rule = "_gotoPage\('(.*?)'\).*?>下一页<"
        tmpStr = self.tool.getRulePageStringOne(page, rule)
        if tmpStr == None:
            self.pageNum = 1
        else:
            self.pageNum = string.atoi(tmpStr) - 1
            if string.atoi(tmpStr) == self.pageNumAll:
                end = 1

    def getTableDataUrl(self, page, rule):
        items = self.tool.getRulePageStringMul(page, rule)
        urlcarry = {}
        for item in items:
            urlcarry[item[1]] = 'http://222.143.24.157' + item[0]
        return urlcarry

    def getTableData(self, urlcarry, classname):
        print classname
        for item in urlcarry:
            print item
            id = '?'+ urlcarry[item].split('?')[1].split('&')[0]
            #thread?
            self.lastdata(id)

    def start(self):
        self.InputExceptionListPage()
        try:
            self.browser.get(self.newurl)
            while True:
                time.sleep(10)
                response = self.browser.page_source.encode('utf-8')
                if self.first == 0:
                    self.getPageNumAll(response)
                    self.first = 1
                self.getPageNum(response)
                rule = 'tb.*?>\s*<a\s*href=\"(.*?)\".*?>(.*?)<'
                tmpUrlData = self.getTableDataUrl(response, rule)
                self.getTableData(tmpUrlData, self.classname)

                if self.pageNum == self.pageNum:
                    break
                else:
                    self.browser.find_element_by_link_text('下一页').click()
            self.close()
        except Exception, e:
            print traceback.print_exc()


if __name__ == "__main__":
    url = 'http://222.143.24.157/search.jspx'
    spider = HeNan(url)

