from django.http import HttpResponse
from django.template import RequestContext,Context, loader
from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from myblog.apps.blog.models import *


def index(request):

    latest_post_list = Post.objects.all().order_by('date')[:5]

    return render_to_response('blog/index.html', {'latest_post_list': latest_post_list}, context_instance=RequestContext(request))

def about(request):
    return render_to_response('blog/about.html', {'title' : "About" }, context_instance=RequestContext(request) )

def code(request):
    return render_to_response('blog/code.html', {'title' : "My codes"}, context_instance=RequestContext(request) )

def contact(request):
    return render_to_response('blog/contact.html', {'title' : "Contact"}, context_instance=RequestContext(request) )


def single_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    return render_to_response('blog/post/post_detail.html', {
                              'post': post},
                               context_instance=RequestContext(request))

