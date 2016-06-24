#!/usr/bin/env python

import sys

try:
    import simplejson as json
except:
    print "manually install simplejson library"
    sys.exit(1)

# Json testing string
json_hash = {"rsp":{"totalResults":"78",
        "items":[
{"cid":"111211","delist_time":"2009-12-08 22:01:26","iid":"1f14014b31fd225cff1c85c926b51a23","nick":"alipublic28","post_fee":"7.00","price":"85.00","title":"one","type":"fixed"},
{"cid":"111211","delist_time":"2009-12-08 22:13:02","iid":"0e9f6930874cac65fc526eba6c7564d2","nick":"alipublic28","post_fee":"7.00","price":"85.00","title":"two","type":"fixed"}
            ]
        }
    }

RSP   = 'rsp'
ITEMS = 'items'
TOTAL = 'totalResults'

class ItemList(object):

    def __init__(self):
        self.total = ""
        self.item = []

    def getTotal(self):
        return self.total
    def setTotal(self, total):
        self.total = total

    def getItem(self):
        return self.item
    def setItem(self, item):
        self.item = item

class Item(object):
    """TaoBao product item model"""

    def __init__(self, nick=None, title=None):
        self.nick   = nick
        self.title  = title

    def getNick(self):
        return self.nick
    def setNick(self, nick):
        self.nick = nick

    def getTitle(self):
        return self.title
    def setTitle(self, title):
        self.title = title

class JSONObject(json.JSONDecoder):
    
    def __init__(self, raw_json):
        super(JSONConvert, self).__init__()
        self.data = raw_json

    def dump(self):
        return self.decode(self.data)

def JSONConvert(dct):
    print dct

    mylist = ItemList()

    rsp = dct.get(RSP, None)

    if rsp and isinstance(rsp, dict):
        total = rsp.get(TOTAL, None)
        if total and isinstance(total, str):
            mylist.setTotal(total)

            itemlist = []
            for item in rsp.get(ITEMS, []):

                this_item = Item(nick=item.get('nick', None), 
                                title=item.get('title', None))
                itemlist.append(this_item)
                
            mylist.setItem(itemlist)

    return mylist

############################
# Main program start here  #
############################

# simple dump
rsp = json.dumps(json_hash, sort_keys=True, indent=4)
print rsp

print "############################"
mylist = json.loads(rsp)
itemList = JSONConvert(mylist)
print itemList.getTotal()
for item in itemList.getItem():
    print item.getTitle(), item.getNick()

