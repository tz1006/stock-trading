#!/usr/bin/python3
# -*- coding: UTF-8 -*- 
# filename: stock.py

from tools import *

class stock():
    def __init__(self, code):
        self.code = code
        self.name = stock_name(code)
    # 停牌
    def status():
    	pass
    # 价格
    def price(self):
        return price_now(self.code)
    # 涨幅
    def wave(self):
        return price_now(self.code)
    # MA
    def MA():
    	return MA
    # 历史价格
    def history():
    	pass



sh600123 = stock('600123')
sh600123.price
