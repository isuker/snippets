#!/usr/bin/env python
#-*- coding: utf-8 -*-
""" 
Frontend for Stock Mangaer

This is a managment tool for your favorate stock pool, which will
nofity you by Fetion or Email when certain trigger is satisfied.

There are two mode:
    1) CLI mode
    2) DEAMON mode

"""

import logging
import time,sys
import signal
from optparse import OptionParser

import report
import database
import stock

log = logging.getLogger("Manager")

# NEED import seetings.py file first!!!
try:
    import settings
except ImportError:
    import sys
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. \n" %__file__)
    sys.exit(1)

class InvalidParam(Exception):
    pass

class FavorStockPool(object):
    """My Favorite Stock Pool"""

    # favorite stock list
    pool = []
    # recycle box list
    recycle = []

    def __init__(self, *args, **kwargs):
    
        self.db = database.FileUtil()
        self.pool = self.db.get_pool()
        self._args = args
        self._kwargs = kwargs

    def add(self, stock):
        """add one stock"""


        if self.exist(stock.code):
            return False

        self.pool.append(stock)
        self.db.add(stock)
        return True

    def exist(self, code):
    
        index = 0
        for s in self.pool:
            if s.code == code:
                return True
        return False

    def remove(self, code):
        """remove one stock"""
        
        index = 0 
        for s in self.pool:
            if s.code == code:
                r = self.pool.pop(index)
                self.recycle.append(r)
                self.db.remove(r.code)
                return True
            index += 1
        # end for
        return False

    def fresh(self, stock=None):
        '''fresh one stack and save to db

            if no stock suppile, just refresh all
        '''

        fresh_list = [stock]
        if not stock:
            fresh_list = self.pool
        for p in fresh_list:

            if p.update():
                self.remove(p.code)
                self.add(p)
        #end for

    def query(self):
        pass
        
    def output(self):
    
        #s = ""
        #for p in self.pool:
        #    s += p.output()
        #    s += "\n"
        #return s
        # or
        #return reduce(lambda x,y: x+"\n"+y,map(lambda p: p.output(), self.pool))
        # or
        sorted_pool = sorted(self.pool, key=lambda s: s.code)
        return "\n".join(map(lambda p: p.output(), sorted_pool))


class StockManager(object):

    MODES = ["CLI", "DEAMON"]

    def __init__(self, *args, **kwargs):

        self.fsp = FavorStockPool()

        # load configure from seetings file
        self.load_confgiure()

    def load_confgiure(self):

        notify_type = settings.NOTIFY_ENABLE and settings.NOTIFY_TYPE

        self.nofitier = None
        if notify_type == "FETION":
            self.notifier = report.Fetioner(settings.NOTIFY_USER, settings.NOTIFY_PASSWORD)
        if notify_type == "EMAIL":
            self.notifier = report.Emailer(settings.NOTIFY_USER, settings.NOTIFY_PASSWORD)
        else:
            self.nofitier = None

        self.receivers = settings.NOTIFY_RECEIVERS

        self.delay = settings.TIME_DELAY

        self.max_counter = settings.MAX_COUNT

    def exec_command(self, parser):

        if not isinstance(parser, OptionParser):
            raise InvalidParam("Not parser in exec_command")
            return

        (options, args) = parser.parse_args()

        #print options, args

        # default print help message
        subcommand = 'help'
        if len(args):
            subcommand = args[0]

        if subcommand == "server":
            self.run()
        elif subcommand == "syncdb":
            self.syncdb()
        elif subcommand == "cli":
            self.run_cli(parser)
        elif subcommand == "help":
            print parser.usage
        else:
            raise InvalidParam("Not support sub-command, valid is server|syncdb|cli|help")

    def syncdb(self):
        '''update the stock pool'''
        return self.fsp.fresh()

    def run_cli(self, parser):
        (options, args) = parser.parse_args()

        mode = options.opt or int(0)
        code = options.code or ""

        price = (0,10000000)
        if options.goal:
            p = options.goal.split(',')
            if len(p) == 2:
                price = (p[0], p[1])
            else:
                raise InvalidParam("goal price format is wrong, should be -g min,max")
        # end if

        if not code and mode in [1,2,4]:
            raise InvalidParam("stock code is missage")

        simple = stock.FavorStock(code)
        simple.setGoalPrice(price)

        existed = self.fsp.exist(code)
        if mode == 1:
            if not existed:
                # get latest price first
                simple.update()
                # Then add to pool
                self.fsp.add(simple)
            else:
                print "%s is alreasy in stock pool, use -e instead"%options.code
        elif mode == 2:
            self.fsp.remove(code)
        elif mode == 3:
            if code == "":
                print self.fsp.output()
            else:
                simple.update()
                print simple.output()
        elif mode == 4:
            if existed:
                self.fsp.fresh(simple)
            else:
                print "%s is not in stock pool" %options.code
        else:
            raise InvalidParam("Not support CLI options")

    def is_working_time(self):

        tt = time.localtime()

        # this is weekend. 
        if tt.tm_wday in [5, 6]:
            return False

        # You konw it: the working time is 9:30 --11:30 and 13:00 -- 15:00
        if tt.tm_hour == 9 and tt.tm_min > 30:
            return True

        if tt.tm_hour == 11 and tt.tm_min < 30:
            return True

        if tt.tm_hour in [10,13,14]:
            return True

        if tt.tm_hour >= 15:
            return False
            
        # otherwise, it's time to sleep
        return False

    def run(self, *args):
        
        log.info( "== StockManager server is starting ==" )
        loop = 0
        while True:

            if not self.is_working_time():
                log.info( "Time to sleep every %s second, do nothing..." %self.delay )
                time.sleep(self.delay)
                continue
            # enf if

            log.info("Monitor stock pool every %s second..." %self.delay)
            time.sleep(self.delay)
            loop += 1
            for stock in self.fsp.pool:

                try:
                    stock.update()
                except Exception, e:
                    log.error( "update stock failed -- %s" %str(e) )
                    # go to handle next stock
                    continue
                # end try

                # check buy/sell point and send message
                (buy, sell) = stock.checkPoint()

                # if users have been notifier too many times, just skip
                # And wait for another LONG time to continue monitor
                if buy and stock.counter < self.max_counter:
                    msg = "BUY %s[%s] %s" %(stock.name, stock.code, stock.price[2])
                    self.notifier.send(self.receivers, msg)
                    stock.notified()
                if sell and stock.counter < self.max_counter:
                    msg = "SELL %s[%s] %s" %(stock.name, stock.code, stock.price[2])
                    self.notifier.send(self.receivers, msg)
                    stock.notified()
                #enf if
            #end for

            # time goes fly and it's time to reset the counter
            if loop == 30:
                loop = 0
                for stock in self.fsp.pool:
                    if stock.counter == self.max_counter:
                        log.info( "clear counter of %s" %str(stock) )
                        stock.clear()

        # end while

        return True

    def query(self, code=[]):
        """query one stock"""
        pass

def option_parser():

    name = sys.argv[0]

    usage="""
    My Private Stock Manager

    %s subcommand [options] [args]

    Available Sub-commands:
      server
      syncdb
      help
      cli

    List of cli commands:
    %s cli [-a][-d][-l][-e] [args]

    -a add     add one stock
    -l list    print one stock
    -e edit    update one stock
    -r remove   delete one stock""" %(name,name)

    parser = OptionParser(usage=usage)

    parser.add_option("-a", "--add", action="store_const", const=1, dest="opt",help="add one stock")
    parser.add_option("-r", "--remove", action="store_const", const=2, dest="opt",help="remove one stock")
    parser.add_option("-l", "--list", action="store_const", const=3, dest="opt",help="list one/all stock")
    parser.add_option("-e", "--edit", action="store_const", const=4, dest="opt",help="update one stock")

    parser.add_option("-c", "--code", dest="code", help="stock code string (like sh600111 or sz002294)")
    parser.add_option("-g", "--goal",dest="goal",help="goal price(like -g 10,20)")

    return parser

def main():

    def signal_handler(signal, frame):
        log.info(" ...You Pressed CTL+C ,exit... ")
        sys.exit(1)
    # end def

    signal.signal(signal.SIGINT, signal_handler)

    manager = StockManager()
    try:
        manager.exec_command(option_parser())
    except InvalidParam,e:
        log.debug( str(e) )

    sys.exit(0)

    # wait for singal
    signal.pause()

if __name__ == "__main__":
    main()
