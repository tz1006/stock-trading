#!/usr/bin/python3
# -*- coding: UTF-8 -*- 
# filename: price-notification/goradar.py
# discription: stocklist.py

import requests
import os
from bs4 import BeautifulSoup
from datetime import datetime
from threading import Thread


class stocklist():
    def __init__(self):
        self.get_list()
    def get_list(self):
        message = '开始导入所有股票到列表。'
        self.__log(message)
        print(message)
        start_time = datetime.now()
        self.list = self.get_sha() + self.get_sza() + self.get_szzx() + self.get_szcy()
        self.list = list(set(self.list))
        end_time = datetime.now()
        timedelsta = (end_time - start_time).seconds
        message = '成功导入%s支股票，耗时%s秒。' % (len(self.list), timedelsta)
        self.__log(message)
        print(message)
    def get_sha(self):
        self.sha = []
        s = requests.session()
        s.keep_alive = False
        start_time = datetime.now()
        url = 'http://query.sse.com.cn/security/stock/getStockListData2.do?&stockType=1&pageHelp.beginPage=1&pageHelp.pageSize=2000'
        header = {
    	  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0',
    	  'Referer': 'http://www.sse.com.cn/assortment/stock/list/share/'
    	  }
        stock_data = s.get(url, headers = header).json()['pageHelp']['data']
        for i in stock_data:
            code = i['SECURITY_CODE_A']
            self.sha.append(code)
        end_time = datetime.now()
        timedelsta = (end_time - start_time).seconds
        message = '从 上海A股 导入%s支股票，耗时%s秒。' % (len(self.sha), timedelsta)
        self.__log(message)
        print(message)
        return(self.sha)
    def get_sza(self):
        self.sza = []
        index_url = 'http://www.szse.cn/szseWeb/FrontController.szse?ACTIONID=7&AJAX=AJAX-FALSE&CATALOGID=1110&TABKEY=tab2&tab2PAGENO=1'
        s = requests.session()
        s.keep_alive = False
        r = s.get(index_url)
        index_html = r.content
        index_soup = BeautifulSoup(index_html, "html.parser")
        index = int(index_soup.select('td')[-3].text.split()[1][1:-1])
        start_time = datetime.now()
        message = '正在获取 深A 列表，一共%s页。' % (index+1)
        #self.__log(message)
        print(message)
        threads = []
        for i in range(index):
            i = i + 1
            a = Thread(target=self.get_sza_page, args=(i,))
            threads.append(a)
            a.start()
        for t in threads:
            t.join()
        end_time = datetime.now()
        timedelsta = (end_time - start_time).seconds
        message = '从 深圳A股 导入%s支股票，耗时%s秒。' % (len(self.sza), timedelsta)
        self.__log(message)
        print(message)
        return(self.sza)
    def get_sza_page(self, page_num):
        url = 'http://www.szse.cn/szseWeb/FrontController.szse?ACTIONID=7&AJAX=AJAX-FALSE&CATALOGID=1110&TABKEY=tab2&tab2PAGENO=%s' % page_num
        s = requests.session()
        s.keep_alive = False
        r = None
        while r == None:
            try:
                r = s.get(url, timeout=10)
            except:
                #message = '载入第%d页码失败' % page_num
                #self.__log(message)
                #print(message)
                pass
        html = r.content
        soup = BeautifulSoup(html, "html.parser")
        source = soup.select('tr[bgcolor="#ffffff"]')
        source1 = soup.select('tr[bgcolor="#F8F8F8"]')
        source += source1
        for i in source:
            code = i.select('td')[2].text
            self.sza.append(code)
    def get_szzx(self):
        self.szzx = []
        index_url = 'http://www.szse.cn/szseWeb/FrontController.szse?ACTIONID=7&AJAX=AJAX-FALSE&CATALOGID=1110&TABKEY=tab5&tab5PAGENO=1'
        s = requests.session()
        s.keep_alive = False
        r = s.get(index_url)
        index_html = r.content
        index_soup = BeautifulSoup(index_html, "html.parser")
        index = int(index_soup.select('td')[-3].text.split()[1][1:-1])
        start_time = datetime.now()
        message = '正在获取 深圳中小板 列表，一共%s页。' % (index+1)
        #self.__log(message)
        print(message)
        threads = []
        for i in range(index):
            i = i + 1
            a = Thread(target=self.get_szzx_page, args=(i,))
            threads.append(a)
            a.start()
        for t in threads:
            t.join()
        end_time = datetime.now()
        timedelsta = (end_time - start_time).seconds
        message = '从 深圳中小板 导入%s支股票，耗时%s秒。' % (len(self.szzx), timedelsta)
        self.__log(message)
        print(message)
        return(self.szzx)
    def get_szzx_page(self, page_num):
        url = 'http://www.szse.cn/szseWeb/FrontController.szse?ACTIONID=7&AJAX=AJAX-FALSE&CATALOGID=1110&TABKEY=tab5&tab5PAGENO=%s' % page_num
        s = requests.session()
        s.keep_alive = False
        r = None
        while r == None:
            try:
                r = s.get(url, timeout=10)
            except:
                #message = '载入第%d页码失败' % page_num
                #self.__log(message)
                #print(message)
                pass
        html = r.content
        soup = BeautifulSoup(html, "html.parser")
        source = soup.select('tr[bgcolor="#ffffff"]')
        source1 = soup.select('tr[bgcolor="#F8F8F8"]')
        source += source1
        for i in source:
            code = i.a.u.text
            self.szzx.append(code)
    def get_szcy(self):
        self.szcy = []
        index_url = 'http://www.szse.cn/szseWeb/FrontController.szse?ACTIONID=7&AJAX=AJAX-FALSE&CATALOGID=1110&TABKEY=tab6&tab6PAGENO=1'
        s = requests.session()
        s.keep_alive = False
        r = s.get(index_url)
        index_html = r.content
        index_soup = BeautifulSoup(index_html, "html.parser")
        index = int(index_soup.select('td')[-3].text.split()[1][1:-1])
        start_time = datetime.now()
        message = '正在获取 深圳创业板 列表，一共%s页。' % (index+1)
        #self.__log(message)
        print(message)
        threads = []
        for i in range(index):
            i = i + 1
            a = Thread(target=self.get_szcy_page, args=(i,))
            threads.append(a)
            a.start()
        for t in threads:
            t.join()
        end_time = datetime.now()
        timedelsta = (end_time - start_time).seconds
        message = '从 深圳创业板 导入%s支股票，耗时%s秒。' % (len(self.szcy), timedelsta)
        self.__log(message)
        print(message)
        return(self.szcy)
    def get_szcy_page(self, page_num):
        url = 'http://www.szse.cn/szseWeb/FrontController.szse?ACTIONID=7&AJAX=AJAX-FALSE&CATALOGID=1110&TABKEY=tab6&tab6PAGENO=%s' % page_num
        s = requests.session()
        s.keep_alive = False
        r = None
        while r == None:
            try:
                r = s.get(url, timeout=10)
            except:
                #message = '载入第%d页码失败' % page_num
                #self.__log(message)
                #print(message)
                pass
        html = r.content
        soup = BeautifulSoup(html, "html.parser")
        source = soup.select('tr[bgcolor="#ffffff"]')
        source1 = soup.select('tr[bgcolor="#F8F8F8"]')
        source += source1
        for i in source:
            code = i.a.u.text
            self.szcy.append(code)
    def __log(self, text):
        text = '%s  %s\n' % (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), text)
        with open('sharelist.log', 'a') as f:
            f.write(text)
    def help(self):
        print('''sl.list\nsl.sha\nsl.sza\nsl.szzx\nsl.szcy\nsl.get_sha()\nsl.get_sza()\nsl.get_szzx()\nsl.get_szcy()\n
            ''')



sl = stocklist()
