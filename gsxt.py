# -*- coding:utf-8 -*-
import sys
import re
import thread
import time
import string
import traceback
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


reload(sys)
sys.setdefaultencoding('utf-8')

class Tool:
    def __init__(self):
        self.removeBody =re.compile('<tbody.*?>|</tbody>')
        self.removeAddr = re.compile('<a.*?>|</a>')
        self.removeLine = re.compile('<tr>|<div>|</div>|</p>|</tr>')
        self.removeTH = re.compile('<thead.*?>|</thead>|<th.*?>|</th>')
        self.replaceTD = re.compile('<td.*?>|</td>')
        self.replaceBR = re.compile('<br><br>|<br>')
        self.removeExtraTag = re.compile('<.*?>')
    def replaceTable(self, x):
        x = re.sub(self.removeBody, "", x)
        x = re.sub(self.removeLine, "", x)
        x = re.sub(self.removeTH, "", x)
        x = re.sub(self.removeAddr, "", x)
        x = re.sub(self.replaceTD, "", x)
        x = x.replace("\t", "").strip()
        return x

class GSXTIndex:
    def __init__(self):
        self.url = 'http://gsxt.saic.gov.cn/'
        self.browser = webdriver.PhantomJS(executable_path='D:\\python\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe')

    def urlCarry(self):
        try:
            self.browser.get(self.url)
            response = self.browser.page_source.encode('utf-8')
            pattern = re.compile('_trackEvent.*?>(.*?)<')
            items = re.findall(pattern,response)
            urlcarry = {}
            for item in items:
                hrefstring = self.browser.find_element_by_link_text(item).get_attribute('href')
                urlcarry[item] = hrefstring
            return urlcarry
        except Exception, e:
            print traceback.print_exc()

    def Close(self):
        return self.browser.quit()

class GSXTPaging:
    def __init__(self, urlsdict):
        self.pageNum = 0
        self.pageNumAll = 0
        self.tool = Tool()
        self.urlcarry = urlsdict
        self.browser = webdriver.PhantomJS(executable_path='D:\\python\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe')

    def findExceptionDirectory_zhejiang(self, url):
        try:
            self.browser.get(url)
            response = self.browser.page_source.encode('utf-8')
            #zhejiang
            pattern = re.compile('(经营异常名录)\s*\$.*?action.*?\"(.*?)\"')
            pageitems = re.findall(pattern, response)
            newurl = 'http://gsxt.zjaic.gov.cn/' + pageitems[0][1]
            return newurl
        except Exception, e:
            print traceback.print_exc()

    def getTableData(self, page):
        pattern = re.compile('(<table.*?>)([\s\S]*?)(</table>)')
        tableData = re.findall(pattern, page)
        print self.tool.replaceTable(tableData[2][1])

    def getPageNumAll(self,page):
        pattern = re.compile('endPage\".*?\"(.*?)\">')
        self.pageNumAll = re.search(pattern, page).group(1)
        #print self.pageNumAll

    def getPageNum(self, page):
        pattern = re.compile('nextPage\".*?\"(.*?)\">')
        pageNum = string.atoi(re.search(pattern, page).group(1)) - 1
        #print pageNum

    def getTableDataUrl(self, page):
        pattern = re.compile('text-align:left.*?false\">(.*?)<')
        items = re.findall(pattern, page)

        urlcarry = {}
        for item in items:
            hrefstring = self.browser.find_element_by_link_text(item).get_attribute('href')
            #异常数据if hrefstring
            urlcarry[item] = hrefstring
            print item, hrefstring
        #return urlcarry

    def getTableCycle(self, newUrl):
        try:
            self.browser.get(newurl)
            time.sleep(3)
            response = self.browser.page_source.encode('utf-8')
            if response != None:
                self.getPageNumAll(response)
                self.getPageNum(response)
                self.getTableData(response)
                self.getTableDataUrl(response)
            else:
                print 'newurl haven\'t open'

        except Exception, e:
            print traceback.print_exc()

    def Close(self):
        return self.browser.quit()

if __name__ == "__main__":
    #get the index urls
    spider = GSXTIndex()
    items = spider.urlCarry()
#    for item in items:
#        print item, items[item]
    spider.Close()
    #
    spider = GSXTPaging(items)
    newurl = spider.findExceptionDirectory_zhejiang('http://gsxt.zjaic.gov.cn/zhejiang.jsp')
    spider.getTableCycle(newurl)
    spider.Close()
