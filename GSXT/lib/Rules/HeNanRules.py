# -*- coding:utf-8 -*-
import requests
import re
import urlparse
import sys

class HENAN:
    def __init__(self, idStr):
        self.run(idStr)

    def run(self):
        print 1