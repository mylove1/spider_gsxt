# -*- coding:utf-8 -*-
import sys
import re
import time
import string
import traceback
from selenium import webdriver

reload(sys)
sys.setdefaultencoding('utf-8')

WORKDIRPATH = 'D:\work\GSXT'
sys.path.append(WORKDIRPATH)
from lib.config import  *

class ZheJiang:
    def __init__(self, url):
        self.url = url
        self.tool = Tool()
        self.pageNum = 0
        self.pageNumAll = 0
        self.first = 0
        self.end = 0
        self.newurl = ''
        self.newurlpaging = ''
        self.classname = 'ZHEJIANGTABLE'
        self.browser = webdriver.PhantomJS(executable_path = PHANTOMJSDIRPATH)

    def close(self):
        return self.browser.quit()

    def InputExceptionListPage(self):
        rule = '(经营异常名录)\s*\$.*?action.*?\"(.*?)\"'
        items = self.tool.getRuleString(self.browser, self.url, rule)
        self.newurl = 'http://gsxt.zjaic.gov.cn/' + items[0][1]
        self.newurlpaging = 'http://gsxt.zjaic.gov.cn/appbasicinfo/doViewAppBasicInfo.do?corpid='


    def getPageNumAll(self,page):
        rule = 'endPage\".*?\"(.*?)\">'
        tmpNum = self.tool.getRulePageStringOne(page, rule)
        if tmpNum == None:
            self.pageNumAll = 1
        else:
            self.pageNumAll = tmpNum
    def getPageNum(self, page):
        if self.end == 1:
            return self.pageNumAll
        rule = 'nextPage\".*?\"(.*?)\">'
        tmpStr = self.tool.getRulePageStringOne(page, rule)
        if tmpStr == None:
            self.pageNum = 1
        else:
            self.pageNum = string.atoi(tmpStr) - 1
        if string.atoi(tmpStr) == self.pageNumAll :
            end = 1

    def getTableDataUrl(self, page, newUrlPaging):
        pattern = re.compile('text-align:left.*?viewDetail\(\'(.*?)\'.*?false\">(.*?)<')
        items = re.findall(pattern, page)
        urlcarry = {}
        for item in items:
            if '{{' in item[1] or '{{' in item[0]:
                continue
            urlcarry[item[1]] = newUrlPaging + item[0] + '&no=7'
        return urlcarry

    def start(self):
        self.InputExceptionListPage()
        try:
            self.browser.get(self.newurl)
            while True:
                # WebDriverWait(self.browser, timeout=10).until(self.has_page_load)
                # self.browser.implicitly_wait(30)
                time.sleep(10)

                response = self.browser.page_source.encode('utf-8')
                if response == None and '{{nextPage}}' in response:
                    print "newurl haven\'t loading!"
                else:
                    if self.first == 0:
                        self.getPageNumAll(response)
                        self.first = 1
                    else:
                        pass
                    self.getPageNum(response)
                    # area carry thread?
                    tmpUrlData = self.getTableDataUrl(response, self.newurlpaging)
                    print tmpUrlData
                    print self.pageNum
                    print self.pageNumAll

                    # newData = self.checkDataIsNew(tmpUrlData)
                    # self.urlPagingCarry.update(newData)

                    # start get the lastData
                    #getLastData(tmpUrlData)

                if self.pageNum == self.pageNumAll:
                    break
                else:
                    self.browser.find_element_by_link_text('下一页').click()
            self.close()
        except Exception, e:
            print traceback.print_exc()


if __name__ == "__main__":
    url  = 'http://gsxt.zjaic.gov.cn/zhejiang.jsp'
    spider = ZheJiang(url).start()
