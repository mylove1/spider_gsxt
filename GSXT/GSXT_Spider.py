# -*- coding:utf-8 -*-
import sys
from multiprocessing import Pool
import importlib

reload(sys)
sys.setdefaultencoding('utf-8')

#WORKDIRPATH = "E:\python_proj"
WORKDIRPATH = "D:\work"

sys.path.append(WORKDIRPATH)
from lib.GSXTIndexUrl import GSXTIndex
from lib.OtherPage.zhejiang import ZheJiang
from lib.OtherPage.guanlizongju import GuanLiZongJu

if __name__ == "__main__":

    #url = 'http://gsxt.saic.gov.cn/'
    #urlCarry = GSXTIndex(url).start()

    urlCarry = { 'GuanLiZongJu':'http://gsxt.saic.gov.cn/zjgs','ZheJiang': 'http://gsxt.zjaic.gov.cn/zhejiang.jsp'}
    p = Pool()
    for item in urlCarry:
        print 'Start %s Get The Data...'
        p.apply_async(globals()[item](urlCarry[item]))
        print 'End %s Get The Data...'
    p.close()
    p.join()

