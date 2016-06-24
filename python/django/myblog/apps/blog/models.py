from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from managers import PostManager

class Category(models.Model):
    title = models.CharField(max_length=250, help_text=_('Maximum 250 '
            'characters.'))
    slug = models.SlugField(unique=True, help_text=_('Suggested value '
            'automatically generated from title. Must be unique.'))
    description = models.TextField()

    class Meta:
        ordering = ['title']
        verbose_name_plural = _('Categories')

    def __unicode__(self):
        return self.title

    def get_post_count(self):
        '''Return the post number under the category'''
        return Post.objects.get_post_by_category(self).count()

class Post(models.Model):

    TYPE_CHOICES = ( 
        ('page', _('Page')),
        ('post', _('Post')),
    )   
    STATUS_CHOICES = ( 
        ('publish', _('Published')),
        ('draft', _('Unpublished')),
    )   

    title = models.CharField(max_length=64)
    slug = models.SlugField(blank=True, null=True, unique=True)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User)
    category = models.ManyToManyField(Category)
    type = models.CharField(max_length=20, default='post', choices=TYPE_CHOICES)
    status = models.CharField(max_length=20, default='publish', choices=STATUS_CHOICES)
    #comments =  generic.GenericRelation(Comment, 
    #                object_id_field='object_pk',
    #                content_type_field='content_type')
    objects = PostManager()
    #tag = TagField()

    def save(self):
        super(Post, self).save()
    
    def __unicode__(self):
        return self.title

    def get_admin_url(self):
        return '/admin/blog/post/%d/' %self.id

    @models.permalink
    def get_absolute_url(self):
        return ('post-single', [str(self.id)])

    def get_author(self):
        try:
            profile = self.author.get_profile()
        except Exception:
            name = self.author.username
        else:
            name = profile.nickname
        
        return name

from django.contrib.comments.moderation import CommentModerator, moderator

class PostModerator(CommentModerator):
    email_notification = True
    auto_close_field   = 'date'
    # Close the comments after 30 days.
    close_after        = 30

    def email(self, comment, content_object, request):

        pass

moderator.register(Post, PostModerator)

