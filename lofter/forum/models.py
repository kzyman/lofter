# -*- coding:utf-8 -*-

import sys

reload(sys)
sys.setdefaultencoding("utf-8")
from django.db.models.signals import post_save
from django.utils.http import urlquote
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation ,GenericForeignKey
from django.template.defaultfilters import slugify
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponse
from django.dispatch import receiver
from django.db.models.signals import post_save
import re

class LofterUser(models.Model):
    users = models.OneToOneField(User, related_name='common_user')
    user_name = models.CharField(max_length=10)
    avatar = models.ImageField(blank=True, null=True)
    description = models.CharField(blank=True, max_length=500)
    follower = models.ManyToManyField('self',symmetrical=False,related_name='user_follower',blank=True)
    following = models.ManyToManyField('self',symmetrical=False,related_name='user_following',blank=True)

    def __unicode__(self):
        return self.user_name


class Tag(models.Model):
    tag = models.CharField(max_length=20, blank=True)

    def __unicode__(self):
        return self.tag


class CategoryManager(models.Manager):
    def get_new_category(self):
        query = self.get_queryset().order_by('-created_date')
        return query

    def get_hot_category(self):
        query = self.get_queryset().order_by('-category__involved')


class Category(models.Model):
    name = models.CharField(unique=True, max_length=20)
    description = models.CharField(max_length=100)
    involved = models.IntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    recommend = models.IntegerField(default=0)
    objects = CategoryManager()

    def __unicode__(self):
        return self.name


class BaseTopicManager(models.Manager):

    def get_hot_topic(self):
        self.get_queryset().order_by('-creted_date')

    def archive_user_all_topic(self,uid):
        dates=set()
        dic={}
        dates = self.get_queryset().created_date
        for date in dates:
            query = self.get_queryset().filter(created_date=date, created_by=uid)
            dic.setdefault(date,[]).append(query)
        return dic





class BaseTopic(models.Model):
    DRAFT = 'D'
    HIDDEN = 'H'
    PUBLISHED = 'P'
    ENTRY_STATUS = (
        (DRAFT, 'Draft'),
        (HIDDEN, 'Hidden'),
        (PUBLISHED, 'Published'),
    )
    category = models.ForeignKey(Category, related_name="category_topic", null=True, blank=True)
    created_by = models.ForeignKey(User, related_name="author_topic")
    title = models.CharField(max_length=20)
    content = models.TextField(null=True,blank=True)
    music = models.URLField(blank=True, null=True)
    music_picture = models.CharField(max_length=300, blank=True)
    vedio = models.URLField(blank=True, null=True)
    recommand_num = models.IntegerField(default=0, blank=True, verbose_name=u'推荐数目')
    created_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=ENTRY_STATUS,default=PUBLISHED)
    tag = models.ManyToManyField(Tag, related_name="tag_topic",blank=True)
    topic_type =models.IntegerField(blank=True,null=True)
    objects = BaseTopicManager()

    def __unicode__(self):
        return self.title

    def save(self,*args, **kwargs):
        self.category.involved +=1
        self.category.save()
        super(BaseTopic,self).save(*args, **kwargs)


class Picture(models.Model):
    topic = models.ForeignKey(BaseTopic, related_name='topic_picture',null=True,blank=True)
    picture = models.ImageField(upload_to='forum/')
    description = models.CharField(max_length=100,null=True,blank=True)

class Reply(models.Model):
    replyer = models.ForeignKey(User, related_name='user_reply')
    content = models.TextField(blank=False)
    topic = models.ForeignKey(BaseTopic, verbose_name=u'所属主题', related_name='topic_reply')
    submit_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(blank=True, null=True, editable=False)
    event = GenericRelation('Event')

    def __unicode__(self):
        return self.topic.title
class Baseinvolved(models.Model):
    owner = models.ForeignKey(User,related_name="%(app_label)s_%(class)s_related",null=True,blank=True)
    involved_topic = models.ForeignKey(BaseTopic,related_name="%(app_label)s_%(class)s_related",null=True,blank=True)
    created_time = models.DateTimeField()
    class Meta:
        abstract =True
    def __unicode__(self):
        self.owner.username




class Favorite(Baseinvolved):
    event = GenericRelation('Event')
    def __unicode__(self):
        return self.owner.username
class subscription(Baseinvolved):#订阅
    involved_category = models.ForeignKey(Category,related_name='category_subscription',)
    def __unicode__(self):
        return self.owner.username

@receiver(post_save, sender=Reply, dispatch_uid='num1')
def event_handler(sender,instance, **kwargs):
    reply = instance
    to_name = re.compile('(?<=@)(\w+)',re.UNICODE)
    handle_to_name = set(re.findall(to_name,reply.content))
    if handle_to_name:
        for name in handle_to_name:
            if name != reply.replyer.users.username:
                try:
                    to_user = User.objects.get(username =name)
                    event = Event(author=reply.replyer,event=reply,to_other=to_user)
                    event.save()
                except:
                    pass
    elif reply.replyer != reply.topic.created_by:
        event =Event(author =reply.replyer,event=reply,to_other =reply.topic.created_by,status=0)
        event.save()


class Event(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    event = GenericForeignKey('content_type', 'object_id')
    author = models.ForeignKey(User, verbose_name=u"发起人")
    status = models.IntegerField()
    is_read = models.BooleanField(default=False, verbose_name=u'已读')
    is_deleted = models.BooleanField(default=False, verbose_name=u'已删除')
    submint_time = models.DateTimeField(auto_now_add=True, verbose_name=u'时间')
    to_other = models.ForeignKey(User, related_name="other", verbose_name=u"提到的人")

    def __unicode__(self):
        return (self.author, self.event.topic, self.to_other)
