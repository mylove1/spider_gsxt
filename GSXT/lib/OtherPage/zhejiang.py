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
        self.newurl = ''
        self.newurlpaging = ''
        self.browser = webdriver.PhantomJS(executable_path = PHANTOMJSDIRPATH)

    def close(self):
        return self.browser.quit()

    def InputExceptionListPage(self):
        rule = '(经营异常名录)\s*\$.*?action.*?\"(.*?)\"'
        items = self.tool.getRuleString(self.browser, self.url, rule)
        self.newurl = 'http://gsxt.zjaic.gov.cn/' + items[0][1]
        self.newurlpaging = 'http://gsxt.zjaic.gov.cn/appbasicinfo/doViewAppBasicInfo.do?corpid='


    def getPageNumAll(self,page):
        pattern = re.compile('endPage\".*?\"(.*?)\">')
        self.pageNumAll = re.search(pattern, page).group(1)

    def getPageNum(self, page):
        pattern = re.compile('nextPage\".*?\"(.*?)\">')
        self.pageNum = string.atoi(re.search(pattern, page).group(1)) - 1

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
                    self.getPageNumAll(response)
                    self.getPageNum(response)
                    # area carry thread?
                    tmpUrlData = self.getTableDataUrl(response, self.newurlpaging)
                    print tmpUrlData
                    print self.pageNum
                    # newData = self.checkDataIsNew(tmpUrlData)
                    # self.urlPagingCarry.update(newData)

                    # start get the lastData
                    # self.getLastData(newData)

                if self.pageNum == self.pageNumAll:
                    break
                else:
                    self.browser.find_element_by_link_text('下一页').click()
        except Exception, e:
            print traceback.print_exc()


if __name__ == "__main__":
    url  = 'http://gsxt.zjaic.gov.cn/zhejiang.jsp'
    spider = ZheJiang(url)
    spider.InputExceptionListPage()
    spider.start()
    spider.close()