# -*- coding:utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

WORKDIRPATH = "E:\python_proj"

sys.path.append(WORKDIRPATH)
from lib.GSXTIndexUrl import GSXTIndex
from lib.OtherPage import *

if __name__ == "__main__":

    url = 'http://gsxt.saic.gov.cn/'
    spider = GSXTIndex()
    urlCarry = spider.start(url)
    """
    for item in urlCarry:
        print urlCarry[item]
        print item
    """
    spider.close()

    url = urlCarry["浙江"]
    print url

    