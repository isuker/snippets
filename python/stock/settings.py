#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
Setting File for Stock Manager

"""

import os.path
import sys

DATABASE_ENGINE = "FILE" # 'postgresql', 'mysql', 'sqlite3'
DATABASE_NAME = "./favor-stock.txt"
DATABASE_USER = ''
DATABASE_PASSWORD = ''

# stock minotor time delay, default is 30s
TIME_DELAY = 30

# MAX counter for NOTIFY
MAX_COUNT = 5


# receviers info
NOTIFY_ENABLE = False    # True or False
NOTIFY_TYPE = "FETION"   # valid value is "FETION" or "EMAIL"
NOTIFY_USER = "138XXXXXXXX"
NOTIFY_PASSWORD = "XXXXXXX"
NOTIFY_RECEIVERS = "xxxxxxxxx0"
