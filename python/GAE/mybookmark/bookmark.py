# -*- coding: utf-8 -*-

from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

import wsgiref.handlers
from time import sleep

total_bookmarks = 0

class BookMark(db.Model):
    address = db.LinkProperty(required=True)
    title = db.StringProperty(required=True)
    tag = db.StringProperty()
    description = db.StringProperty(multiline=True)
    shared = db.BooleanProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    post_id= db.IntegerProperty()

class MainPage(webapp.RequestHandler):

    def get(self):

        bookmarks = BookMark.all()
        count = bookmarks.count()

        global total_bookmarks
        total_bookmarks = count
        html_data = template.render('templates/index.html', {'bookmark_list' : 
                                    bookmarks, 'count' : count})
        self.response.out.write(html_data )

    def post(self):
        pass

class Error404(webapp.RequestHandler):
    def get(self):
        self.error(404)
        #self.redirect("/index")

class RemoveBookMark(webapp.RequestHandler):

    def get(self):
        remove_id  = self.request.get('remove_id')
        #self.response.out.write("remove%s" %remove_id)

        bookmark = BookMark.all().filter('post_id = ', int(remove_id)).fetch(1)
        #this_bookmark = bookmark.key()
        for item in bookmark:
            global total_bookmarks
            total_bookmarks -= 1

            message = "<p>remove %s sucessfully!</p>" %item.title
            self.response.out.write(message)
            item.delete()

        # wait for 3 seconds
        #sleep(3)    
        self.redirect("/")

    def post(self):
        bookmark = BookMark.all().fetch(1000)
        #this_bookmark = bookmark.key()
        for item in bookmark:
            global total_bookmarks
            total_bookmarks -= 1

            message = "<p>remove %s sucessfully!</p>" %item.title
            self.response.out.write(message)
            item.delete()

        # wait for 3 seconds
        #sleep(3)    
        self.redirect("/")

class EditBookMark(webapp.RequestHandler):

    def get(self):
        pass

    def post(self):
        pass

class AddBookMark(webapp.RequestHandler):

    def get(self):

        message = u'收藏新网址'
        html_data = template.render('templates/add_bookmark.html', {'info' : message})
        self.response.out.write(html_data )

    def post(self):

        address = "http://raychen1984.cublog.cn/"
        title = "my personal blog"
        if not self.request.get('address'): 
            pass
        else:
            address = self.request.get('address')

        if not self.request.get('title'): 
            pass
        else:
            title = self.request.get('title')

        tag = self.request.get('tag')
        description = self.request.get('description')
        shared = self.request.get('shared')
        if ( shared  == "public" ) :
            shared = True
        if ( shared == "private" ) :
            shared = False

        global total_bookmarks
        total_bookmarks += 1
        this_bookmark = BookMark(address=address,
                                 title=title,
                                 tag=tag,
                                 shared=shared,
                                 description=description)
        # store this bookmark into database
        this_bookmark.put()

        # update the key of model
        this_bookmark.post_id =  this_bookmark.key().id()
        this_bookmark.put()
        self.redirect("/")

application = webapp.WSGIApplication([('/', MainPage), 
                                      ('/add', AddBookMark),
                                      ('/del', RemoveBookMark),
                                      ('/edit', EditBookMark),
                                      ('.*',Error404)], 
                                      debug=True)


def main():
        #print "start main"
        #run_wsgi_app(application)
        #global total_bookmarks
        #total_bookmarks = 0
        wsgiref.handlers.CGIHandler().run(application)

if __name__ == "__main__":
    main()
