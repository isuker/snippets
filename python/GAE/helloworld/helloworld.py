from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

import wsgiref.handlers
import taobao

import os
#os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
#from django.conf import settings
#settings._target = None

class TaobaoProduct(db.Model):
    title = db.StringProperty()
    nick = db.StringProperty()
    pic_url = db.LinkProperty()
    price = db.StringProperty()
    click_url = db.StringProperty()

class MainPage(webapp.RequestHandler):

    def get(self):

        #self.response.headers['Content-Type'] = 'text/plain'
        # get taobao product from OpenAPI
        # See taobao.py for more details
        data = taobao.get_taobao_data()
        my_product_list = taobao.dump_data(data)

        # Store data to databases
        for item in my_product_list:
            one_product = TaobaoProduct(title=item['title'],    
                                        nick=item['nick'],
                                        pic_url=item['pic_url'],
                                        price=item['price'],
                                        click_url=item['click_url'])
            # save this product
            one_product.put()
            #print "save" , one_product.title

        # get all products in database
        products = TaobaoProduct.all()
        count = products.count()
        html_data = template.render('table.html', {'product_list' : products, 'count' : count})
        self.response.out.write(html_data )

class Error404(webapp.RequestHandler):
    def get(self):
        self.error(404)
        #self.redirect("/index")

application = webapp.WSGIApplication([('/', MainPage), 
                                      ('.*',Error404)], 
                                      debug=True)

def main():
        #print "start main"
        #run_wsgi_app(application)
        wsgiref.handlers.CGIHandler().run(application)

if __name__ == "__main__":
    main()
