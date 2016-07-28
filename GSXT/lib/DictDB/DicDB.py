# -*- coding:utf-8 -*-
import re
import sys
import traceback
import redis

reload(sys)
sys.setdefaultencoding('utf-8')

class DicDB:
    def __init__(self):
        #self.Dic = redis.StrictRedis(host='localhost', port=6379, db=0)
        self.Dic = {}
        pass

    def setDic(self, key, value):
        if not self.Dic.exists(key):
            self.Dic.set(key, value)

    def getDic(self, key):
        if self.Dic.exists(key):
            return self.Dic.get(key)

    def delDicValue(self, key):
        if self.Dic.exists(key):
            self.Dic.delete(key)

    def DBSize(self):
        return self.Dic.dbsize()

    def saveDb(self):
       return  self.Dic.save()

    def DelAllValue(self):
        return  self.Dic.flushdb()
