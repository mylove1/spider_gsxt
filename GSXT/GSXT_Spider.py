# -*- coding:utf-8 -*-
import sys
from multiprocessing import Pool

reload(sys)
sys.setdefaultencoding('utf-8')

#WORKDIRPATH = "E:\python_proj"
WORKDIRPATH = "D:\work"

sys.path.append(WORKDIRPATH)
from lib.GSXTIndexUrl import GSXTIndex
from lib.OtherPage import zhejiang

if __name__ == "__main__":

    url = 'http://gsxt.saic.gov.cn/'
    urlCarry = GSXTIndex(url).start()
    for item in urlCarry:
        print item
        print urlCarry[item]

    p = Pool()
    for item in urlCarry:
        p.apply_async(item(urlCarry[item].start()), args=(item,))
    p.close()
    p.join()

