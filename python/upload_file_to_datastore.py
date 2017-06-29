#!/usr/bin/env python
# This is the urllib2 version for example in case of no requests library: 
#   https://github.com/vmware/pyvmomi-community-samples/blob/master/samples/upload_file_to_datastore.py
# https://docs.python.org/2/howto/urllib2.html

from __future__ import print_function  # This import is for python2.*
import atexit
#import requests
import httplib
import urllib
import urllib2
import cookielib
import argparse
import os.path
import ssl

# https://stackoverflow.com/questions/14207708/ioerror-errno-32-broken-pipe-python
#from signal import signal, SIGPIPE, SIG_DFL
#signal(SIGPIPE, SIG_DFL)

import atexit
import mmap
import base64


from pyVim import connect
from pyVmomi import vim
from pyVmomi import vmodl

# https://dellaert.org/2015/12/02/pyvmomi-6-0-0-vsphere-6-0-and-ssl/
# http://www.errr-online.com/index.php/2015/05/09/how-to-fix-ssl-issues-with-pyvmomi-and-python-2-7-9/
try:
   _create_default_https_context = ssl._create_unverified_context
except:
   # This version doesn't validate certificates anyway
   pass
else:
   ssl._create_default_https_context = _create_default_https_context


class MethodRequest(urllib2.Request):
    def __init__(self, *args, **kwargs):
        if 'method' in kwargs:
            self._method = kwargs['method']
            del kwargs['method']
        else:
            self._method = None
        return urllib2.Request.__init__(self, *args, **kwargs)

    def get_method(self, *args, **kwargs):
        if self._method is not None:
            return self._method
        return urllib2.Request.get_method(self, *args, **kwargs)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--datastore',
                        required=True,
                        action='store',
                        help='Datastore name')
    parser.add_argument('-l', '--local_file',
                        required=True,
                        action='store',
                        help='Local disk path to file')
    parser.add_argument('-r', '--remote_file',
                        required=True,
                        action='store',
                        help='Path on datastore to place file')
    parser.add_argument('-S', '--disable_ssl_verification',
                        required=False,
                        action='store_true',
                        help='Disable ssl host certificate verification')
    parser.add_argument('-H', '--host', required=True, action='store')
    parser.add_argument('-u', '--user', default='root', action='store')
    parser.add_argument('-p', '--password', default='ca$hc0w', action='store')
    args = parser.parse_args()

    return args


def main():

    args = get_args()

    try:
        service_instance = None
        #context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        #context.verify_mode = ssl.CERT_NONE
        try:
            service_instance = connect.SmartConnect(host=args.host,
                                                    user=args.user,
                                                    pwd=args.password,)
                                                    #sslContext=context)
        except IOError as e:
            pass
        if not service_instance:
            print("Could not connect to the specified host using specified "
                  "username and password")
            raise SystemExit(-1)

        # Ensure that we cleanly disconnect in case our code dies
        atexit.register(connect.Disconnect, service_instance)

        content = service_instance.RetrieveContent()
        session_manager = content.sessionManager

        # Get the list of all datacenters we have available to us
        datacenters_object_view = content.viewManager.CreateContainerView(
            content.rootFolder,
            [vim.Datacenter],
            True)

        # Find the datastore and datacenter we are using
        datacenter = None
        datastore = None
        for dc in datacenters_object_view.view:
            datastores_object_view = content.viewManager.CreateContainerView(
                dc,
                [vim.Datastore],
                True)
            for ds in datastores_object_view.view:
                if ds.info.name == args.datastore:
                    datacenter = dc
                    datastore = ds
        if not datacenter or not datastore:
            print("Could not find the datastore specified")
            raise SystemExit(-1)
        # Clean up the views now that we have what we need
        datastores_object_view.Destroy()
        datacenters_object_view.Destroy()

        # Build the url to put the file - https://hostname:port/resource?params
        if not args.remote_file.startswith("/"):
            remote_file = "/" + args.remote_file
        else:
            remote_file = args.remote_file
        resource = "/folder" + remote_file
        params = {"dsName": datastore.info.name,
                  "dcPath": datacenter.name}
        http_url = "https://"+args.host+":443"+resource+"?%s" %urllib.urlencode(params)

        # Get the cookie built from the current session
        client_cookie = service_instance._stub.cookie
        # Break apart the cookie into it's component parts - This is more than
        # is needed, but a good example of how to break apart the cookie
        # anyways. The verbosity makes it clear what is happening.
        cookie_name = client_cookie.split("=", 1)[0]
        cookie_value = client_cookie.split("=", 1)[1].split(";", 1)[0]
        cookie_path = client_cookie.split("=", 1)[1].split(";", 1)[1].split(
            ";", 1)[0].lstrip()
        cookie_text = " " + cookie_value + "; $" + cookie_path
        # Make a cookie
        cookie = dict()
        cookie[cookie_name] = cookie_text

        # Create a password manager for the Basic Auth request
        urlRoot = "https://%s/folder" % (args.host)
        passmgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
        passmgr.add_password(None, urlRoot, args.user, args.password)
        # Install the handler.  Oddly, this is global (?)
        authhndlr = urllib2.HTTPBasicAuthHandler(passmgr)
        httpsHandler = urllib2.HTTPSHandler(debuglevel=1)
        httpHandler = urllib2.HTTPHandler(debuglevel=1)
        opener = urllib2.build_opener(authhndlr,httpHandler,httpsHandler)
        urllib2.install_opener(opener)
        
        # another way to use cookie
        #opener.addheaders.append(('Cookie', '%s=%s'%(cookie_name, cookie_text)))

        # Get the file to upload ready, extra protection by using with against
        # leaving open threads
        fd = open(args.local_file, 'rb')
        atexit.register(fd.close)
        data = mmap.mmap(fd.fileno(), 0, access=mmap.ACCESS_READ)
        atexit.register(data.close)

        request = urllib2.Request(http_url, data)
        request.add_header('Content-Type', 'application/octet-stream')
        request.add_header('Content-Length', str(len(data)))
        # directly use 'Authorization' in header. can ingore authhndlr
        request.add_header("Authorization", "Basic %s" % base64.b64encode("%s:%s" % (args.user, args.password)))
        #request.add_header('Connection', 'keep-alive')
        request.get_method = lambda: 'PUT'  # Hackery.  Use 'PUT' instead of 'POST'
        #request.unverifiable=args.disable_ssl_verification
        #resp = opener.open(request) # can use urlopen directly after install_opener
        resp = urllib2.urlopen(request)

        # another way to use object
        #request = MethodRequest(url, method='PUT', data,headers=headers, unverifiable=args.disable_ssl_verification) 

    except httplib.BadStatusLine as e:
        print("Ingore caught httplib.BadStatusLine fault : " + str(e))
    except vmodl.MethodFault as e:
        print("Caught vmodl fault : " + e.msg)
        raise SystemExit(-1)


if __name__ == "__main__":
    main()
    print('work done')
