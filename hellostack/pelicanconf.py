#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import os

CWD=os.path.abspath(os.curdir)

AUTHOR = u'Ray Chen'
SITENAME = u'Hello Stack'
SITEURL = 'http://hellostack.me'

PATH = 'content'

TIMEZONE = 'Asia/Shanghai'

DEFAULT_LANG = u'en'
DATE_FORMATS = {
    'en': '%a, %d %b %Y',
    'zh_cn': '%Y-%m-%d(%a)',
}

#THEME = "bootstrap2"
#THEME = "/home/ray/hellostack/pelican-themes/simple-bootstrap"
THEME = os.path.join(CWD, "pelican-themes/pelican-bootstrap3")
SITESUBTITLE = "Cloud,Python,Automation,Fedora/Linux"
GITHUB_URL = "https://github.com/crook"
#GITHUB_USER = "crook"
GITHUB_SHOW_USER_LINK = True
DISQUS_SITENAME = "hellostack"
#DISQUS_DISPLAY_COUNTS = True
GOOGLE_ANALYTICS = 'UA-51314242-1'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/%s.atom.xml'
TRANSLATION_FEED_ATOM = 'feeds/all-%s.atom.xml'

PYGMENTS_STYLE = 'manni'
BOOTSTRAP_NAVBAR_INVERSE = True
#ABOUT_ME = 'about.html'

DISPLAY_TAGS_ON_SIDEBAR = True
DISPLAY_TAGS_INLINE = True

#MENUITEMS = (
#    ('RSS', 'http://hellostack.me/feeds/all.atom.xml'),
#    ('About', 'http://hellostack.me/about.html'),
#
#)

# Blogroll
LINKS = (
    (u'小企鹅看大世界', 'http://chenrano2002.blog.chinaunix.net/'),
    ('Feisky\'s Blog', 'http://feisky.xyz'),
    ('Wang Xu\'s Blog', 'http://wangxu.me'),
    ('Lyndon\'s Blog', 'http://www.hellospark.me/'),
    ('Openstack', 'http://www.openstack.org/'),
)

# Social widget
SOCIAL = (
    ('Github', 'https://github.com/crook'),
    ('Weibo', 'http://weibo.com/crookcrook/'),
    ('RSS', 'http://hellostack.me/feeds/all.atom.xml'),
)

DEFAULT_PAGINATION = 10
DISPLAY_ARTICLE_INFO_ON_INDEX = True

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
