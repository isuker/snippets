#!/usr/bin/python

import threading
import time,random
import sys,traceback
import signal

# flag for work done
work_done=False
DEBUG=False

# flag if you want to kill others after first one done
KILLALL=False

class T(threading.Thread):
    """A worker thread template"""
    def __init__(self, func, name="T",*args, **kwargs):
        self.__name = name
        self.__func = func
        self.__args = args
        self.__kwargs = kwargs
        self.__return = None

        super(T, self).__init__(verbose=DEBUG)

    def run(self):
        '''overtide thread's run routines'''

        # get a random time, else set time to 1 second
        t = self.__kwargs.get("time", 1)
        print "%s[%s] starts running" %(self.__name, t)

        try:
            self_return = self.__func(self.__name, *self.__args, **self.__kwargs)
        except:
            print "call %s failed" %self.__func
            traceback.print_exc()

        # if work done, send singal to kill others

    @property
    def output(self):
        return self.__return

def test_who_finish_work_first():

    start = threading.Event()
    stop = threading.Event()

    def signal_handler(signal, frame):

        print "Got CTL+C, exit"
        raise SystemExit
    # end

    signal.signal(signal.SIGINT, signal_handler)

    def F(name, *args, **kwargs):

        global work_done
        #print name, work_done,args, kwargs

        t = kwargs.get("time", 1)

        print "%s: is start? %s" %(name,start.isSet())

        print "%s:  wait for main thread say start" %name
        # wait for main thread to say start
        start.wait()

        # start to do work, and the finished time is random
        print "%s: bababa...doing something"%name
        time.sleep(t)
        work_done = True

        # notify Main thread that: I'm done, you can kill others
        stop.set()
        print "%s: done! pls MAIN kill others" %name

        return name
            
    # end def

    #############################

    pool = []

    for item in range(5):
        name = "T%s" %item
        # set a random time for work during
        t = random.randint(1,8)
        pool.append(T(F, name, time=t))

    for t in pool:
        start.clear()
        stop.clear()
        t.start()

    # wait for worker is ready for job
    time.sleep(2)

    ######## Main thread #########
    start.set()
    
    print "MAIN: ok, mutil-work start"

    # want for the first thread to finish job
    stop.wait()
    if stop.isSet():
        print "MAIN: %s, just exit main thread " %work_done
        # kill all active thread
        for t in threading.enumerate():
                print "stop thread %s[%s]" %(t.getName(),t.ident)
                try:
                    if KILLALL == True:
                        t._Thread__stop()
                    pass
                except:
                    print str(t.getName())+ "could not be terminated"

        # normal exit from main thread
        print "exit entry"
        sys.exit(0)
    else:
        print "MAIN: still wait for stop event"

    print "ERROR: shouldn't get here"
    
if __name__ == "__main__":
    test_who_finish_work_first()
