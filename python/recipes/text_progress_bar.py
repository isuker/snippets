#!/usr/bin/python
#
#  Show text progress bar (like wget output) when axel download
#

import time,os,os.path
from urlgrabber.progress import TextMeter
import subprocess
import threading

PWD = os.path.abspath(os.path.dirname(__file__))

DATA = "http://download-cf.jetbrains.com/python/pycharm-community-3.1.2.tar.gz"

FILENAME = "pycharm-community-3.1.2.tar.gz"
SIZE = 108405591

class Axel(threading.Thread):

    def run(self):
        ret = subprocess.call(['axel', '-q', DATA, '-o', FILENAME ])
        return ret


def get_size(filename):
    return os.path.getsize(os.path.join(PWD,filename))


# MAIN
a = Axel()
a.start()
time.sleep(2)

# start 
tm = TextMeter()
tm.start(filename=FILENAME, text=FILENAME)

cur = get_size(FILENAME)
while True:

    if cur >= SIZE:
        print "Done"
        break

    cur = get_size(FILENAME)
    print "size: %d" %cur
    tm.update(cur)
    time.sleep(1)

tm.end(SIZE)
a.join()

