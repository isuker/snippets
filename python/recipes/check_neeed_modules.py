#!/usr/bin/python
# 
#   Decorator to check if needed modules for method are imported 
#   And load the module if possible

import sys
import inspect
import time

def import_required_modules(func, name):
    """ Decorator to check if needed modules for method are 
    imported And load the module if possible
    """
    print "try to load %s module for func:%s" %(name, repr(func))
    def wrapper(*args, **kwargs):

        # if catch ImportError exception, we should know
        # how to do now

        print "import %s modules" %name
        if len(args):
            if inspect.isfunction(args[0]):
                print "first argument must be the function:%s"%args[0]
            else:
                print "why not it function??"
        # if

        frame = inspect.currentframe()
        print inspect.getargvalues(frame)
        __import__(name)

    print "call fun:%s before return" %str(func)

    return wrapper

def get_time(*args, **kwargs):
    """return time"""
    print args
    print kwargs
    return time.time()
get_time_old = import_required_modules(get_time, "time")

def test_old_decorator():
    print get_time_old()
    print get_time_old(name=5)
    print get_time_old("time")
    print get_time_old(lambda x:2*x)
    print get_time_old("time", 'sys', name=5)

###############################################
def import_required(name):

    def wrapper(f, *args, **kwargs):
        print "Call %s" %f.func_name

        try:
            __import__(name)
        except ImportError, e:
            print "import %s failed" %name

        frame = inspect.currentframe()
        print inspect.getargvalues(frame)
        return f

    return wrapper


@import_required('time')
def get_time2(*args, **kwargs):
    print args
    print kwargs
    return time.time()

def test_get_time2():

    print get_time2()
    print get_time2(hello="world")
    print get_time2("hello", "world")
    print get_time2("hello", "world", name='ray')


###############################################
def import_required_modules_with_params(name):

    print "try to load %s module" %name
    def function(f):

        print "function name:%s" %f.func_name
        def wrapper(*arg, **kwargs):

            print "import %s modlues" %name
            __import__(name)

            frame = inspect.currentframe()
            print inspect.getargvalues(frame)

        return wrapper

    return function

@import_required_modules_with_params('time')
#@import_required_modules('time')
def get_time_new(*arg, **kwargs):
    """return time"""
    print args
    print kwargs
    return time.time()

def test_decorator():
    print get_time_new()
    print get_time_new(name=5)
    print get_time_new("time")
    print get_time_new("time", 'sys', name=5)

class myDecorator(object):
    """class decorator"""

    def __init__(self, fn):
        print "inside __init__"
        self.fn = fn
    def __call__(self):
        print "inside before __call__"
        self.fn()
        print "inside after __call__"

@myDecorator
def fun():
    print "inside fun"

class myDecoratorWithParam(object):
    """class decorator"""

    def __init__(self, url):
        print "inside P.__init__"
        #self.fn = fn
        self.route = url
    def __call__(self, fn):
        print "inside before P.__call__"
        def wrapper(*args):
            print "inside wrapper"
            fn(self.route+str(args))
        return wrapper
        print "inside after P__call__"

@myDecoratorWithParam("route")
def route(name="blank"):
    print "inside route to %s" %name


if __name__ == "__main__":

    print "======================="
    test_old_decorator()
    print "======================="
    test_get_time2()
    print "======================="
    test_decorator()
    print "======================="
    fun()
    route()
    route("index")
