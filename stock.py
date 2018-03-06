#!/usr/bin/python3
# -*- coding: UTF-8 -*- 
# filename: stock.py

from tools import *

class stock():
    def __init__(self, code):
        self.code = code
        self.name = stock_name(code)
        self.open_price = 0
    # 价格
    def price(self):
        return price_now(self.code)
    # 涨幅
    def wave(self):
        return price_now(self.code)
    def t():





sh600123 = stock('600123')
sh600123.price
