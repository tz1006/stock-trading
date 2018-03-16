#!/usr/bin/python3
# -*- coding: UTF-8 -*- 
# filename: stock_all.py
# description: Stock-trade
# version: V1


import requests
import os
from bs4 import BeautifulSoup
from datetime import datetime
from pytz import timezone
from threading import Thread
import json
from concurrent.futures import ThreadPoolExecutor




class stock():
    def __init__(self, code):
        self.__s = requests.session()
        self.__s.keep_alive = False
        self.code = code
        self.sscode = self.__sscode()
        self.name = self.__name()
        self.status = self.__status()
        #self.open = gap(code)[0]
        #self.high = gap(code)[1]
        #self.low = gap(code)[2]
        #self.close = close(code)
        self.__get_index()
    # 停牌
    def __status(self):
        url = 'https://apiapp.finance.ifeng.com/stock/isopen?code=%s' % self.sscode
        r = None
        while r == None:
            try:
                r = self.__s.get(url, timeout=5)
            except:
            	pass
        isopen = r.json()['data'][0]['isopen']
        if isopen == 1:
            return True
        else:
            return False
    # sh600123
    def __sscode(self):
        code = str(self.code)
        if code[0]+code[1] =='60':
            code = 'sh%s' % code
        else:
            code = 'sz%s' % code
        return code
    # 股票名
    def __name(self):
        url = 'http://hq.sinajs.cn/list=%s' % self.sscode
        r = None
        while r == None:
            try:
                r = self.__s.get(url, timeout=5)
            except:
            	pass
        name = r.text.split("\"")[1].split(",",1)[0]
        return name
    # (价格, 均价)
    def price(self):
        url = 'http://api.finance.ifeng.com/aminhis/?code=%s&type=five' % self.sscode
        r = None
        while r == None:
            try:
                r = self.__s.get(url, timeout=5)
            except:
                pass
        if r.text == '':
            #print('无法获取 %s 价格。' % stock_code)
            price = ''
            average = ''
        else:
            now = r.json()[-1]['record'][-1]
            # date
            date = now[0].split(' ')[0]
            # Price
            price = float(now[1])
            # diff
            diff = float(now[2])
            # Average
            average = float(now[4])
        return (price, average)
    # (涨幅, 价格波动)
    def wave(self):
        url = 'https://hq.finance.ifeng.com/q.php?l=%s' % self.sscode
        #print(url)
        r = None
        while r == None:
            try:
                r = self.__s.get(url, timeout=5)
            except:
                pass
        j = json.loads(r.text.split('=', 1)[1].split(';')[0])
        data = j[list(j)[0]]
        price = data[0]
        price_diff = data[2]
        wave = data[3]
        return (wave, price_diff)
    # 涨幅2
    # MA 当日 (ma5, ma10, ma20, ma30)
    def __get_index(self):
        url = 'http://suggest.eastmoney.com/SuggestData/Default.aspx?type=1&input=%s' % self.code
        r = self.__s.get(url)
        self.__index = r.text.split(',')[-2]
        today = datetime.now(timezone('Asia/Shanghai'))
        self.__today = ['%d' % today.year, '%02d' % today.month, '%02d' % today.day]
    def ma(self):
        span = '%s%s%s' % (self.__today[0], self.__today[1], self.__today[2])
        url = 'http://pdfm.eastmoney.com/EM_UBG_PDTI_Fast/api/js?id=%s%s&TYPE=k&rtntype=1&QueryStyle=2.2&QuerySpan=%s%%2C1&extend=ma' % (self.code, self.__index, span)
        #print(url)
        r = None
        while r == None:
            try:
                r = self.__s.get(url, timeout=5)
            except:
                pass
        if r.text == '({stats:false})':
            return
        else:
            date = r.text.split(',', 1)[0].split('(')[1]
            today = '%s-%s-%s' % (self.__today[0], self.__today[1], self.__today[2])
            if date == today:
                ma_data = r.text.split('[')[1].split(']')[0].split(',')
                ma5 = float(ma_data[0])
                ma10 = float(ma_data[1])
                ma20 = float(ma_data[2])
                ma30 = float(ma_data[3])
                return(ma5, ma10, ma20, ma30)
            else:
                return
    # KDJ 当日 (k, d, j)
    def kdj(self):
        span = '%s%s%s' % (self.__today[0], self.__today[1], self.__today[2])
        url = 'http://pdfm.eastmoney.com/EM_UBG_PDTI_Fast/api/js?id=%s%s&TYPE=k&rtntype=1&QueryStyle=2.2&QuerySpan=%s%%2C1&extend=kdj' % (self.code, self.__index, span)
        #print(url)
        r = None
        while r == None:
            try:
                r = self.__s.get(url, timeout=5)
            except:
                pass
        if r.text == '({stats:false})':
            return
        else:
            date = r.text.split(',', 1)[0].split('(')[1]
            today = '%s-%s-%s' % (self.__today[0], self.__today[1], self.__today[2])
            #today = '2018-03-15'
            if date == today:
                kdj_data = r.text.split('[')[1].split(']')[0].split(',')
                k = float(kdj_data[0])
                d = float(kdj_data[1])
                j = float(kdj_data[2])
                return(k, d, j)
            else:
            	return
    def macd(self):
        span = '%s%s%s' % (self.__today[0], self.__today[1], self.__today[2])
        url = 'http://pdfm.eastmoney.com/EM_UBG_PDTI_Fast/api/js?id=%s%s&TYPE=k&rtntype=1&QueryStyle=2.2&QuerySpan=%s%%2C1&extend=macd' % (self.code, self.__index, span)
        #print(url)
        r = None
        while r == None:
            try:
                r = self.__s.get(url, timeout=5)
            except:
                pass
        if r.text == '({stats:false})':
            return
        else:
            date = r.text.split(',', 1)[0].split('(')[1]
            today = '%s-%s-%s' % (self.__today[0], self.__today[1], self.__today[2])
            #today = '2018-03-15'
            if date == today:
                macd_data = r.text.split('[')[1].split(']')[0].split(',')
                dif = float(macd_data[0])
                dea = float(macd_data[1])
                macd = float(macd_data[2])
                return(dif, dea, macd)
            else:
            	return
    def history(self):
        pass
    def help(self):
        print('''
        .code
        .name
        .status
        .close
        .open
        .high
        .low
        .price()
        .wave()
        .ma()
        .kdj()
        .macd
        .help
    ''')






class stocklist():
    def __init__(self):
        self.get_list()
    def get_list(self):
        message = '尝试从文件导入股票'
        self.__log(message)
        try:
            self.list = self.get_list_from_txt()
        except:
            self.dl_list()
    def get_list_from_txt(self):
        with open('database/stocklist.txt', 'r') as f:
            data = f.read()
        li = json.loads(data)
        message = '文件导入%s支股票' % len(li)
        self.__log(message)
        return li
    def save_list_to_txt(self):
        data = json.dumps(self.list)
        if os.path.exists('database') == False:
            os.makedirs('database')
        with open("database/stocklist.txt","w") as f:
            f.write(data)
        message = '保存%s支股票到文件' % len(self.list)
        self.__log(message)
    def dl_list(self):
        message = '从网络下载股票'
        self.__log(message)
        start_time = datetime.now()
        self.list = self.get_sha() + self.get_sza() + self.get_szzx() + self.get_szcy()
        self.list = list(set(self.list))
        end_time = datetime.now()
        timedelsta = (end_time - start_time).seconds
        message = '成功导入%s支股票，耗时%s秒。' % (len(self.list), timedelsta)
        self.__log(message)
        self.save_list_to_txt()
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
        message = '%s  %s\n' % (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), text)
        if os.path.exists('log') == False:
            os.makedirs('log')
        with open('log/stocklist.log', 'a') as f:
            f.write(message)
        print(text)
    def help(self):
        print('''sl.list\nsl.sha\nsl.sza\nsl.szzx\nsl.szcy\nsl.get_sha()\nsl.get_sza()\nsl.get_szzx()\nsl.get_szcy()\n
            ''')




        
        
class worklist():
    def __init__(self):
        self.list = []
        message = '开始加载股票到wl，一共%s个' % len(sl.list)
        print(message)
        start_time = datetime.now()
        self.__load()
        end_time = datetime.now()
        timedelsta = (end_time - start_time).seconds
        message = '已加载%s支股票，耗时%s秒' %(len(self.list), timedelsta)
        print(message)
    def __load(self):
        self.list.clear()
        with ThreadPoolExecutor(max_workers=4) as executor:
            executor.map(self.add, sl.list)
        self.__drop()
    def __drop(self):
        c = 0
        for i in wl.list:
            if i.status == False:
                wl.list.remove(i)
                c += 1
        message = '移除%s个停牌股票' % c
        print(message)
    def add(self, i):
        a = stock(i)
        self.list.append(a)
        print(i)
        #return a



# sl = stocklist()

sl = stocklist()
wl = worklist()







import code
code.interact(banner = "", local = locals())

