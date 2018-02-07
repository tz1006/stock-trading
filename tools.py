#!/usr/bin/python3
# -*- coding: UTF-8 -*- 
# filename: tools.py


# 工具集
import requests
from datetime import datetime
from pytz import timezone
import json

timeout = 6

s = requests.session()
s.keep_alive = False

########--Tools--########

def sscode(code):
    code = str(code)
    if code[0]+code[1] =='60':
        code = 'sh%s' % code
    else:
        code = 'sz%s' % code
    return code

def share_name(code):
    url = 'http://hq.sinajs.cn/list=%s' % sscode(code)
    r = None
    while r == None:
        r = s.get(url, timeout=timeout)
    name = r.text.split("\"")[1].split(",",1)[0]
    return name

def share_market(code):
    code = str(code)
    if code[0] =='6':
        return('沪市主板')
    elif code[0] =='3':
        return('创业板')
    else:
        if code[2] == '0':
            return('深市主板')
        else:
            return('中小板')

def share_market_code(code):
    code = str(code)
    if code[0] =='6':
        return('SHA')
    elif code[0] =='3':
        return('SZCY')
    else:
        if code[2] == '0':
            return('SZA')
        else:
            return('SZZX')


#######---get-data---#######

def price_now(stock_code):
    url = 'http://api.finance.ifeng.com/aminhis/?code=%s&type=five' % sscode(stock_code)
    r = None
    while r == None:
        try:
            r = s.get(url, timeout=timeout)
        except:
            pass
    if r.text == '':
        print('无法获取 %s 价格。' % stock_code)
        price = ''
        average = ''
    else:
        now = r.json()[-1]['record'][-1]
        # Price
        price = float(now[1])
        # Average
        average = float(now[4])
    return (price, average)


def ma_now(stock_code, debug=0):
    type_url = 'http://suggest.eastmoney.com/SuggestData/Default.aspx?type=1&input=%s' % stock_code
    type_r = None
    while type_r == None:
        try:
            type_r = s.get(type_url, timeout=timeout)
        except:
            pass
    type = type_r.text.split(',')[-2]
    today = datetime.now(timezone('Asia/Shanghai'))
    span = '%s%02d%02d' % (today.year, today.month, today.day)
    url = 'http://pdfm.eastmoney.com/EM_UBG_PDTI_Fast/api/js?id=%s%s&TYPE=k&rtntype=1&QueryStyle=2.2&QuerySpan=%s%%2C1&extend=ma' % (stock_code, type, span)
    #print(url)
    r = None
    while r == None:
        try:
            r = s.get(url, timeout=timeout)
        except:
            pass
    if debug != 0:
        return r
    if r.text == '({stats:false})':
        ma5 = ''
        ma10 = ''
        ma20 = ''
    else:
        ma_data = r.text.split('[')[1].split(']')[0].split(',')
        ma5 = float(ma_data[0])
        ma10 = float(ma_data[1])
        ma20 = float(ma_data[2])
        ma30 = float(ma_data[3])
    #print(ma5, ma10)
    return(ma5, ma10, ma20, ma30)


def ma_hist(stock_code, days=10, debug=0):
    #ua_mo = 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_1_1 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/11.0 Mobile/15B150 Safari/604.1'
    #header = {'User-Agent':ua_mo}
    url = 'http://api.finance.ifeng.com/akdaily/?code=%s&type=last' % sscode(stock_code)
    r = None
    while r == None:
        try:
            r = s.get(url, timeout=timeout)
        except:
            pass
    if debug != 0:
        return r
    ma = r.json()['record']
    ma5 = []
    ma10 = []
    ma20 = []
    date = []
    if ma == {}:
        pass
    else:
        if len(ma) < days:
            pass
        else:
            for l in range(days):
                ma5.append(float(ma[-l-1][8]))
                ma10.append(float(ma[-l-1][9]))
                ma20.append(float(ma[-l-1][10]))
                date.append(datetime.strptime(ma[-l-1][0], '%Y-%m-%d').strftime("%b-%d"))
                #date.append(ma[-l-1][0].split('-',1)[1])
    return(ma5, ma10, ma20, date)


def kdj_now(code, day=1, debug=0):
    type_url = 'http://suggest.eastmoney.com/SuggestData/Default.aspx?type=1&input=%s' % code
    type_r = None
    while type_r == None:
        try:
            type_r = s.get(type_url, timeout=timeout)
        except:
            pass
    type = type_r.text.split(',')[-2]
    today = datetime.now(timezone('Asia/Shanghai'))
    span = '%s%02d%02d' % (today.year, today.month, today.day)
    url = 'http://pdfm.eastmoney.com/EM_UBG_PDTI_Fast/api/js?id=%s%s&TYPE=k&QueryStyle=2.2&QuerySpan=%s%%2C%s&extend=kdj' % (code, type, span, day)
    r = None
    while r == None:
        try:
            r = s.get(url, timeout=timeout)
        except:
            pass
    if debug != 0:
        return r
    result = []
    if r.text == '({stats:false})':
        pass
    else:
        source = r.text[1:-3].split('\r\n')
        for i in range(day):
            i = i + 1
            kdj = source[-i].split('[')[1].split(']')[0].split(',')
            result.append((float(kdj[0]), float(kdj[1]), float(kdj[2])))
    #print(result)
    return(result)


def macd_now(code, day=1, debug=0):
    type_url = 'http://suggest.eastmoney.com/SuggestData/Default.aspx?type=1&input=%s' % code
    type_r = None
    while type_r == None:
        try:
            type_r = s.get(type_url, timeout=timeout)
        except:
            pass
    type = type_r.text.split(',')[-2]
    today = datetime.now(timezone('Asia/Shanghai'))
    span = '%s%02d%02d' % (today.year, today.month, today.day)
    url = 'http://pdfm.eastmoney.com/EM_UBG_PDTI_Fast/api/js?id=%s%s&TYPE=k&QueryStyle=2.2&QuerySpan=%s%%2C%s&extend=macd' % (code, type, span, day)
    r = None
    while r == None:
        try:
            r = s.get(url, timeout=timeout)
        except:
            pass
    if debug != 0:
        return r
    result = []
    if r.text == '({stats:false})':
        pass
    else:
        source = r.text[1:-3].split('\r\n')
        for i in range(day):
            i = i + 1
            macd = source[-i].split('[')[1].split(']')[0].split(',')
            result.append((float(macd[0]), float(macd[1]), float(macd[2])))
    #print(result)
    return(result)


def ma_now(code, day=1, debug=0):
    type_url = 'http://suggest.eastmoney.com/SuggestData/Default.aspx?type=1&input=%s' % code
    type_r = None
    while type_r == None:
        try:
            type_r = s.get(type_url, timeout=timeout)
        except:
            pass
    type = type_r.text.split(',')[-2]
    today = datetime.now(timezone('Asia/Shanghai'))
    span = '%s%02d%02d' % (today.year, today.month, today.day)
    url = 'http://pdfm.eastmoney.com/EM_UBG_PDTI_Fast/api/js?id=%s%s&TYPE=k&QueryStyle=2.2&QuerySpan=%s%%2C%s&extend=ma' % (code, type, span, day)
    r = None
    while r == None:
        try:
            r = s.get(url, timeout=timeout)
        except:
            pass
    if debug != 0:
        return r
    result = []
    if r.text == '({stats:false})':
        pass
    else:
        source = r.text[1:-3].split('\r\n')
        for i in range(day):
            i = i + 1
            ma = source[-i].split('[')[1].split(']')[0].split(',')
            result.append((float(ma[0]), float(ma[1]), float(ma[2])))
    #print(result)
    return(result)


def wave_hist(code, rate=0, day=100):
    url = 'http://api.finance.ifeng.com/akdaily/?code=%s&type=last' % sscode(code)
    r = s.get(url)
    d = {}
    li = r.json()['record']
    if len(li) < 100:
        #print('%s少于100天' % code)
        return(d)
    else:
        for i in range(100):
            i = i + 1
            date = li[-i][0]
            wave = float(li[-i][7])
            #如果跌幅超过百分之5
            if rate > wave:
                t = 2
            elif -rate < wave:
                t = 1
            else:
                t = 0
            d[date] = t
        return(d)


def wave_hist(code, rate=0, day=100):
    d = {}
    li = ld_json(code)['record']
    if len(li) < 100:
        #print('%s少于100天' % code)
        return(d)
    else:
        for i in range(100):
            i = i + 1
            date = li[-i][0]
            wave = float(li[-i][7])
            #如果跌幅超过百分之5
            if rate > wave:
                t = 2
            elif -rate < wave:
                t = 1
            else:
                t = 0
            d[date] = t
        return(d)

def ld_json(code):
    with open("json/%s.json" % code,'r') as load_f:
        j = json.load(load_f)
    return(j)

def compare(code1, code2, rate=0, day=100):
    data1 = wave_hist(code1, rate, day)
    data2 = wave_hist(code2, rate, day)
    date = []
    for i in list(data1):
        if i in list(data2):
            date.append(i)
    c = 0
    if len(date) == 0:
        return(0, 0)
    for i in date:
        if data1[i] == data2[i]:
            c += 1
    #print(c, len(date))
    result = c / len(date)
    return(result, len(date))


def contrast(code1, code2, rate=3, day=100):
    data1 = wave_hist(code1, rate, day)
    data2 = wave_hist(code2, rate, day)
    date = []
    for i in list(data1):
        if i in list(data2):
            date.append(i)
    c = 0
    if len(date) == 0:
        return(0, 0)
    for i in date:
        if data1[i] + data2[i] == 3:
            c += 1
    #print(c, len(date))
    result = c / len(date)
    return(result, len(date))




# HELP

def help():
    print('''
# tools
sscode(code)
share_name(code)
share_market(code)
share_market_code(code)
# data-tools
price_now(stock_code)
ma_now(stock_code)
ma_hist(stock_code, days=10)
kdj_now(code,day=1)
macd_now(code,day=1)
compare(code1, code2, rate=0, day=100)
contrast(code1, code2, rate=3, day=100)
  wave_hist(code, rate=0, day=100)
    ''')



if __name__ == '__main__':
    import code
    code.interact(banner = "", local = locals())
