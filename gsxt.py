# -*- coding:utf-8 -*-
import sys
import re
import thread
import time
import string
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


reload(sys)
sys.setdefaultencoding('utf-8')

class Tool:
    def __init__(self):
        self.removeBody =re.compile('<tbody.*?>|</tbody>')
        self.removeAddr = re.compile('<a.*?>|</a>')
        self.removeLine = re.compile('<tr>|<div>|</div>|</p>|</tr>')
        self.removeTHEAD = re.compile('<thead.*?>|</thead>')
        self.removeTH = re.compile('<th.*?>')
        self.removeT = re.compile('\t|\n')
        self.removeExtraTag = re.compile('<.*?>')
        self.removeTD = re.compile('</td>')
        self.replaceTD = re.compile('<td.*?>')
        self.replaceTH = re.compile('</th>')
    def replaceTable(self, x):
        x = re.sub(self.removeT, "", x)
        x = re.sub(self.removeBody, "", x)
        x = re.sub(self.removeAddr, "", x)
        x = re.sub(self.removeTHEAD, "", x)
        x = re.sub(self.replaceTD, "\n", x)
        x = re.sub(self.removeLine, "", x)
        x = re.sub(self.removeTD, "", x)
        x = re.sub(self.removeTH, "", x)
        x = re.sub(self.replaceTH, "\n", x)
        x = self.removeString(x.strip(), "序号\n企业名称\n注册号\n列入日期\n列入经营异常名录原因\n")
        x = x.split("\n")
        for item in x:
            if item == "":
                x.remove(item)
        return x
    def removeString(self, string, errorstr):
        return string.replace(errorstr, "")

    def list_tuple(self, list):
        newList = []
        for i in range(0, len(list),5):
            tmp = list[i:i + 5]
            newList.append(tuple(tmp))
        return newList
    def tmpSaveTableData(self, filepath, tabledata):
        f = open(filepath, "w")
        for temp in tabledata:
            f.write("%s %s\n" % (tabledata[temp], temp))
        f.close()

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
    def __init__(self, urlsIndexdict):
        self.pageNum = 0
        self.pageNumAll = 0
        self.tool = Tool()
        self.urlindexcarry = urlsIndexdict
        self.urlPagingCarry = {}
        self.browser = webdriver.PhantomJS(executable_path='D:\\python\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe')
    #alone
    def findExceptionDirectory_zhejiang(self, url):
        try:
            self.browser.get(url)
            response = self.browser.page_source.encode('utf-8')
            #zhejiang
            pattern = re.compile('(经营异常名录)\s*\$.*?action.*?\"(.*?)\"')
            pageitems = re.findall(pattern, response)
            newurl = 'http://gsxt.zjaic.gov.cn/' + pageitems[0][1]
            newurlpaging = 'http://gsxt.zjaic.gov.cn/appbasicinfo/doViewAppBasicInfo.do?corpid='
            return newurl, newurlpaging
        except Exception, e:
            print traceback.print_exc()

    def getTableData(self, page):
        pattern = re.compile('(<table.*?>)([\s\S]*?)(</table>)')
        tableData = re.findall(pattern, page)
        list= self.tool.replaceTable(tableData[2][1])
        tup = self.tool.list_tuple(list)
        tableTime = {}
        for it in tup:
            tableTime[it[1]] = it[3]
        return tableTime

    def getPageNumAll(self,page):
        pattern = re.compile('endPage\".*?\"(.*?)\">')
        self.pageNumAll = re.search(pattern, page).group(1)
        #print self.pageNumAll

    def getPageNum(self, page):
        pattern = re.compile('nextPage\".*?\"(.*?)\">')
        self.pageNum = string.atoi(re.search(pattern, page).group(1)) - 1
        #print pageNum

    def getTableDataUrl_zhejiang(self, page, newUrlPaging):
        pattern = re.compile('text-align:left.*?viewDetail\(\'(.*?)\'.*?false\">(.*?)<')
        items = re.findall(pattern, page)
        urlcarry = {}
        for item in items:
            if '{{' in item[1] or '{{' in item[0]:
                continue
            urlcarry[item[1]] = newUrlPaging + item[0] + '&no=7'
        return urlcarry

    def getTableCycle(self, newUrl, newUrlPaging):
        try:
            self.browser.get(newUrl)
            while True:
                time.sleep(10)
                #element = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.ID, "myDynamicElement")))
                response = self.browser.page_source.encode('utf-8')
                if response == None and '{{nextPage}}' in response:
                    print "newurl haven\'t loading!"
                else:
                    self.getPageNumAll(response)
                    self.getPageNum(response)
                    if self.pageNum == 1:
                        tableData = self.getTableData(response)
                        self.tool.tmpSaveTableData(TmpData, tableData)
                    print self.pageNum
                    self.urlPagingCarry = self.getTableDataUrl_zhejiang(response, newUrlPaging)
                    print self.urlPagingCarry

                if self.pageNum == self.pageNumAll:
                    break
                else:
                    self.browser.find_element_by_link_text('下一页').click()
        except Exception, e:
            print traceback.print_exc()
    def checkCompanyName(self, CompanyNameCarry):
        pass

    def Close(self):
        return self.browser.quit()

if __name__ == "__main__":
    TmpData = "./Conf/table.txt"

    #get the index urls
    spider = GSXTIndex()
    items = spider.urlCarry()
#    for item in items:
#        print item, items[item]
    spider.Close()

    #zhejiang
    spider = GSXTPaging(items)
    newurl, newurlpaging = spider.findExceptionDirectory_zhejiang('http://gsxt.zjaic.gov.cn/zhejiang.jsp')
    #print newurl
    #print newurlpaging
    spider.getTableCycle(newurl, newurlpaging)
    spider.Close()
