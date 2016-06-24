#!/usr/bin/env python
#
# Description: demo codes to show call function in parallel
#
# Author : Ray Chen (chenrano2002@gmail.com)
# Date : 2011-04-21

import os,sys,time,random
import threading

DEBUG = False

def run_function_in_parallel(func_list):
    for fun_thread in func_list:
        if not isinstance(fun_thread, FuncThread):
            continue
        fun_thread.start()
    # wait all thread finish
    for fun_thread in func_list:
        if not isinstance(fun_thread, FuncThread):
            continue
        fun_thread.join()
    # end for

class FuncThread(threading.Thread):
    """Class of using threading to run function"""
    def __init__(self, function, *args, **kwargs):
        self._function = function
        self._args     = args
        self._kwargs   = kwargs
        # the return value of this function
        self.__return   = None
        threading.Thread.__init__(self,verbose=DEBUG)
        
    def __str__(self):
        s = []
        s.append("function name: " + str(self._function) )
        s.append("turple optional parameters:" + str(self._args) )
        s.append("dict optional parameters:" + str(self._kwargs) )
        return '\n'.join(s)

    def run(self):
        """override threading's run routines"""
        try:
            self.__return = self._function(*self._args, **self._kwargs)
        except:
            print "call %s failed" %self._function
            pass

    @property            
    def output(self):
        return self.__return

class Action(object):
    """
        Action object to encapsulate calling functions
    """
 
    def __init__(self, function, *args, **kwargs):
        self.function = function
        self.args     = args
        self.kwargs   = kwargs
 
    def __str__(self):
        s = []
        s.append("function name: " + str(self.function) )
        s.append("turple optional parameters:" + str(self.args) )
        s.append("dict optional parameters:" + str(self.kwargs) )
        return '\n'.join(s)
 
    def do(self):
 
        ret = None
        if callable(self.function):
            if DEBUG:
                print "call %s " %self.function

            try:
                ret = self.function(*self.args, **self.kwargs)
            except:
                if DEBUG:
                    print "call function failed, type = %s, value = %s, \
                          trackback = %s"%(sys.exc_info())
                pass
        return ret
 
class ActionList(list):
    """
        Action List Handle
    """
 
    def __init__(self, actions=[]):
        self.action_list = actions
 
    def add(self, action):
        if isinstance(action, Action):
            self.action_list.append(action)
 
    def do_in_parallel(self):
 
        if len(self.action_list) == 1:
            return self.action_list[0].do()
 
        pid_list = []
        ret_list = []
        for action in self.action_list:
            pid = os.fork()
            if pid > 0:
                # parent process
                if DEBUG:
                    print "parent process, push %d..." %pid
                pid_list.append(pid)
            else:
                # child process
                if DEBUG:
                    print "run child process: %d..." %os.getpid()
                ret = action.do()
                ret_list.append(ret)
 
                # finish this child process
                sys.exit(0)
        # end for
 
        # Parent process wait for all Child process over
        for pid in pid_list:
            if DEBUG:
                print "wait for %d" %pid
            os.waitpid(pid, os.WNOHANG)
 
        return ret_list
 
def do_action_in_parallel(action_list):
    actions = ActionList(action_list)
    return actions.do_in_parallel()

if __name__ == "__main__":

    print "======start testing========="

    def funA(word):
        time.sleep(random.randint(1, 6))
        print "say", word
        return word

    def funB(config={}):
        time.sleep(random.randint(1, 6))
        print config
        return config

    def funC(key, *args):
        time.sleep(random.randint(1, 6))
        print key, args
        return (key, args)

    def funD(key, *args, **kwargs):
        time.sleep(random.randint(1, 6))
        print key, args, kwargs
        return [key, args, kwargs]

    a = Action(funA, "hello, funA")
    b = Action(funB, {"name":"funB"})
    c = Action(funC, 1, "optional", "funC")
    d = Action(funD, 2, "optional", {"name":"funD"}, index=1)

    ac = ActionList()
    ac.add(a)
    ac.add(b)
    ac.add(c)
    ac.add(d)
    print ac.do_in_parallel()

    time.sleep(25)
    print "======another handy way to run========="
    print do_action_in_parallel([a,b,c,d])   

    time.sleep(25)
    print "=====try threading to run mutil function======"
    fa = FuncThread(funA, "hello, funA")
    fb = FuncThread(funB, {'name':"funB"})
    fc = FuncThread(funC, 1, "optional", "funC")
    fd = FuncThread(funD, 2, {'name':'funD'}, index=1)
    run_function_in_parallel([fa, fb, fc, fd])
    print fa.output, fb.output, fc.output, fd.output
