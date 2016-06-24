#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
A Stock Class

"""

import urllib2
from common import _s, _f, u

class Stock(object):

    # 股票价格 (今日开盘价，昨天收盘价，当前价格，最高价，最低价)
    DEFAULT_PRICE = ("0","0","0","0","0")

    # website
    SINAJS = "http://hq.sinajs.cn/list=%s"

    def __init__(self, code, name="", price=DEFAULT_PRICE):

        # stock code
        self.code = code
        # stock name, UNICODE??
        self.name = name
        # 股票价格 (今日开盘价，昨天收盘价，当前价格，最高价，最低价)
        self.price = price

    def __str__(self):
        '''used for str'''
        return "%s[%s]" %(self.name, self.code)

    def setPrice(self, price):
        if isinstance(price, tuple):
            self.price = _s(price)
        else:
            self.price = DEFAULT_PRICE

    def toString(self, sep=","):
        '''format all data property to string with separator'''
    
        li = [self.code, self.name]
        li.extend(self.price)
        
        # the separator must be string, or set to default ","
        if not isinstance(sep, str):
            sep = ","
        return sep.join(li)

    def output(self):
        return self.toString(sep="\t")

    def update(self):
        """fresh to get real time stock info"""
        try:
            response = urllib2.urlopen(self.SINAJS %self.code)
        except urllib2.URLError, e:
            print "urlopen %s failed --"%self.code, str(e)
            return False
        
        # remove the double qutotation from a string
        html = response.read().strip().replace('\"', "")
        # hq_str_sh600111
        self.code = html.split("=")[0].split()[1].split("_")[2]
        if not self.code:
            return False

        ps = html.split("=")[1].split(",")
        # the webiste code is "GBK" and convert to utf-8
        self.name = ps[0].decode("GBK").encode('utf-8')
        self.setPrice(tuple(ps[1:6]))
        return True

class FavorStock(Stock):
    """My Favorite Stock Pool"""

    def __init__(self, *args, **kwargs):
        super(FavorStock ,self).__init__(*args, **kwargs)

        # The Goal price to buy/sell
        self.goal_price = ("0", "10000000")

        #Flag for buy or sell point
        self.__buy = self.__sell = False

        # flag to show it's alreday buyed or selled.
        self.__buyed = self.__selled = False

        # notified counter
        self.__counter = 0

    # some handy property
    sellable = property(fget=lambda self: self.__sell)
    buyable  = property(fget=lambda self: self.__buy)
    counter  = property(fget=lambda self: self.__counter) 

    def clear(self):
        self.__counter = 0

    def notified(self, plus=True):

        if plus:
            self.__counter +=1
        else:
            self.__counter -= 1
            if self.__counter < 0:
                self.__counter = 0

    def setGoalPrice(self, price):

        if isinstance(price, tuple):
            self.goal_price = _s(price)
        else:
            self.goal_price = ("0", "10000000")

    def setBuyed(self, delay=10):
        """Buy flag to indicate that message has been
            sent out, so DO NOT interrupt me again in delay time
        """
        self.__buyed = True
            
        
    def setSelled(self):
        self.__selled = True

    def checkPoint(self):

        self.__buy = self.__sell = False

        # check buy point
        current_price = _f(self.price[2])
        if current_price < _f(self.goal_price[0]):
            self.__buy = True
            self.setBuyed()
        if current_price > _f(self.goal_price[1]):
            self.__sell = True
            self.setSelled()

        return (self.buyable, self.sellable)

    def toString(self, sep=","):
        '''format all data property to string with separator'''

        li = [self.code, self.name]
        li.extend(self.price)
        li.extend(self.goal_price)
        
        # the separator must be string, or set to default ","
        if not isinstance(sep, str):
            sep = ","
        return sep.join(li)

if __name__ == "__main__":

    stock = FavorStock("sh600111")
    stock.setPrice(('1','2','3','4','5'))
    stock.update()
    print stock, stock.buyable
    stock.setGoalPrice(price=('50', '60'))
    print stock.output()
    print stock.toString("|")

    print stock.checkPoint()


