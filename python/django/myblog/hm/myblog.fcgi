#!/ramdisk/bin/python

import os
import sys

PROJECT_ROOT = "/home1/drawbigf/public_html/blog"
BLOG_ROOT = "/home1/drawbigf/public_html/blog/myblog"

# Add a custom Python path.
sys.path.insert(0, "/home1/drawbigf/lib/python2.4/site-packages/")
# seems like flup egg can't be found in web view, so tell it.
sys.path.insert(0, "/home1/drawbigf/lib/python2.4/site-packages/flup-1.0.3.dev_20100221-py2.4.egg")
sys.path.insert(0, "/home1/drawbigf/lib/python2.4/site-packages/pysqlite-2.6.0-py2.4-linux-x86_64.egg")
sys.path.insert(0, "/home1/drawbigf/lib/python2.4/site-packages/setuptools-0.7a1dev_r0-py2.4.egg")
sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, BLOG_ROOT)

# Switch to the directory of your project. (Optional.)
os.chdir(BLOG_ROOT)

# Set the DJANGO_SETTINGS_MODULE environment variable.
os.environ['DJANGO_SETTINGS_MODULE'] = "myblog.settings"

from django.core.servers.fastcgi import runfastcgi
runfastcgi(method="threaded", daemonize="false")
