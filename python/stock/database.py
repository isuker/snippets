#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
Stock Database Class

"""

import stock
import StringIO

from common import _s

class DBUtil(object):

    def __init__(self, *args, **kwargs):
        pass

    def load(self):
        raise NotImplementedError("Not implement yet!")

class MysqlUtil(DBUtil):
    pass

class FileUtil(DBUtil):

    FAVOR_STOCK_FILE = "favor-pool.txt"

    def __init__(self, filename=FAVOR_STOCK_FILE , *args, **kwargs):
    
        super(FileUtil, self).__init__(*args, **kwargs);
        self.filename = filename

        self.load()

    def add(self, stock):
    
        line = stock.toString()
        with open(self.filename, "a") as f:
            f.write(line+"\n")
    
    def remove(self, code):

        import tempfile,shutil,os
        temp = tempfile.NamedTemporaryFile(delete=False)
        with open(self.filename, "r") as f:
            for line in f:
                line = line.strip()
                if line.startswith("#") or line == "":
                    temp.write(line+"\n")
                    continue
                # handle
                new = line.replace('\"', "")
                pieces = new.split(",")
                if pieces[0] == code:
                    # remove this line, just prefix some '#' chars
                    line = "####" + line
                temp.write(line+"\n")
                    
        # delete temp file and copy
        temp.close()
        shutil.copyfile(temp.name, self.filename)
        os.unlink(temp.name)


    def load(self):
    
        self.stock_pool = []
        with open(self.filename) as f:
            for line in f:
                line = line.strip()
                if line.startswith("#") or line == "":
                    continue

                # handle
                line = line.replace('\"', "")
                pieces = line.split(",")
                s= stock.FavorStock(code=pieces[0], name=pieces[1])
                s.setPrice(tuple(pieces[2:7]))
                s.setGoalPrice(tuple(pieces[-2:]))
                self.stock_pool.append(s)

        return self.stock_pool

    def get_pool(self):
        return self.stock_pool

    def output(self):
        return "\n".join(map(lambda p: p.output(), self.stock_pool))

if __name__ == "__main__":
    fu = FileUtil()
    print fu.output()
    
    s = stock.FavorStock("sh600112")
    s.setPrice(_s((1,2,3,4,5)))
    s.setGoalPrice(price=_s((30, 60))) 
    fu.add(s)

    fu.remove("sh600112")
