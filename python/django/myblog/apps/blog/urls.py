from django.conf.urls.defaults import *
from myblog.apps.blog import views

urlpatterns = patterns('myblog.apps.blog.views',
    # Example:
    # (r'^mysite/', include('mysite.foo.urls')),
    (r'^$', 'index'),
    (r'^about/$', 'about'),
    (r'^code/$', 'code'),
    (r'^contact/$', 'contact'),
    (r'^archives/$', 'index'),
    url(r'^archives/(?P<post_id>\d+).html$', 'single_post',name="post-single"),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

)
