#!/usr/bin/env python
#-*- coding: utf-8 -*-

import threading, time  

class Boy(threading.Thread):  
    def __init__(self, cond, name):  
        super(Boy, self).__init__(verbose=True)  
        self.cond = cond  
        self.name = name  
      
    def run(self):  
        self.cond.acquire()     
        print self.name + ":got lock"
        print self.name +': 嫁给我吧！？'  
        self.cond.notify() #唤醒一个挂起的线程，让hanmeimei表态 
        print self.name +':notify，请hanmeimie表态'
        self.cond.wait() #释放内部所占用的琐，
        print self.name + ':同时线程被挂起，直至接收到通知被唤醒或超时，等待hanmeimei回答'

        print self.name +': 我单下跪，送上戒指！'  
        self.cond.notify()  
        self.cond.wait()
           
        print self.name +': Li太太，你的选择太明治了。'    
        print self.name + ":release lock"
        self.cond.release()
            
class Girl(threading.Thread):  
    def __init__(self, cond, name):  
        super(Girl, self).__init__(verbose=True)  
        self.cond = cond  
        self.name = name  
    def run(self):  
        self.cond.acquire()  
        print self.name + ":got lock"
        self.cond.wait()#等待Lilei求婚  
        print self.name +': 没有情调，不够浪漫，不答应'  
        self.cond.notify()  
        print self.name +':notify, 请lilei表态'
        self.cond.wait()    
        print self.name +': 好吧，答应你'
        self.cond.notify() 
        print self.name + ":release lock"
        self.cond.release() 
            
cond = threading.Condition()  
boy = Boy(cond, 'LiLei')  
girl = Girl(cond, 'HanMeiMei')  

# PS: must call girl thread first
girl.start()
boy.start()  

#boy.join()
#girl.join()
