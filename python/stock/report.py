#!/usr/bin/env python
#-*- coding: utf-8 -*-
""" 
A Reporter class

Report message in real time by Fetion or Email

"""
import sys
import smtplib
import socket
import common
import logging

log = logging.getLogger("Reporter")

# PyWapFetion is got from "https://github.com/whtsky/PyWapFetion"
from PyWapFetion import *

class Report(object):
    """A reporter Base Class"""

    def __init__(self, account, password, *arg, **kwargs):
        self.account = account
        self.password = password

    def send(self, receivers=[], message=""):
        raise NotImplementedError("Not implement yet!")

class Emailer(Report):
    """Email Reporter"""

    SUPPORT_SMTP = ["163", "gmail"]
    GMAIL_SMTP_SERVER = "smtp.gmail.com"
    SMTP_163_SERVER = "smtp.163.com" 

    def __init__(self, account, password):
        super(Emailer, self).__init__(account, password)

        self.login()

    def __def__(self):
        self.stmp.close()

    def login(self):

        self._login = False
        self.stmp = smtplib.SMTP()

        # TODO: Gmail need to handle speical password
        # right now, tempily use 163 stmp server
        try:
            self.stmp.connect(self.SMTP_163_SERVER)
        except socket.error, e:
            log.error(str(e))
            return

        try:
            self.stmp.login(self.account, self.password)
        except smtplib.SMTPException, e:
            log.error(str(e))

        self._login = True
        return

    def send(self, receivers=[], message=""):
        if isinstance(receivers, (str)):
            receivers = ["%s"%receivers]
        elif not isinstance(receivers, list):
            log.debug("Invalid params")
            return

        if not self._login:
            log.warning("Not login yet")
            return

        #self.stmp.docmd("STARTTLS")

        output = {}
        msg = '''
            From: stockManager@notifer.com
            Subject: Auto StockManager Notifer
            Text: %s
        ''' %message
        try:
            output = self.stmp.sendmail(self.account, receivers, msg)
        except Exception, e:
            log.debug(str(e))

        if output:
            log.warning("sent to %s failed" %output.keys())

class Fetioner(Report):
    """Fetion Notifer"""

    def __init__(self, account, password):
        super(Fetioner, self).__init__(account, password)

        self.login()

    def __def__(self):
        self.fetion.logout()

    def login(self):

        self._login = False

        try:
            self.fetion = Fetion(self.account, self.password)
            self._login = True
        except Exception, e:
            log.debug("fetion login failed")
            log.error(str(e))

        self._login = True

    def send(self, receivers=[], message=""):

        if not self._login:
            log.debug("Not login yet")
            return

        if isinstance(receivers, (str)):
            receivers = ["%s"%receivers]
        elif not isinstance(receivers, list):
            log.debug("Invalid params")
            return

        # send this message to all receviers.
        for f in receivers:
            # do nothong except waiting for fetion to login...
            # FIXME!!!
            try:
                self.fetion.send(f, message)
            except:
                pass

            try:

                if self.fetion.send(f, message):
                    log.info("send '%s' to '%s' sucessfully"%(message, f))
                else:
                    log.info( "send '%s' to '%s' failed"%(message, f))
            except Exception, e:
                log.error("skip send '%s' to %s" %(message, f))
            #end try
        # end for
    
    def send2me(self, message=""):
        self.send(receivers=[self.account], message=message)

if __name__ == "__main__":

    log.info('start to test')

    #fetion = Fetioner("phone", "password")
    #fetion.send(["139XXXXXXXX"], "来自list测试信息，请忽略")
    #fetion.send(["139XXXXXXXX", "136XXXXXXXX"], "来自2 list测试信息，请忽略")
    #fetion.send("139XXXXXXXX", "来string测试信息，请忽略")
    #fetion.send2me("from ray self")

    #sys.exit()

    #e = Emailer("XXXXXXXX@gmail.com", "password")
    #e.send("XXXXXXXX@gmail.com", message="test from Emailer")

    _163 = Emailer("XXXXXXXXX@163.com", "password")
    _163.send("XXXXXXXXX@163.com", message="test from Emailer")


