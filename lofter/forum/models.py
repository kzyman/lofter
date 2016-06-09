# -*- coding:utf-8 -*-

import sys,os
from functools import partial
reload(sys)
sys.setdefaultencoding("utf-8")
from django.db.models.signals import post_save,pre_delete,post_delete
from django.db import models
from django.db.models import Prefetch ,Q
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
    user_name = models.CharField(max_length=10,null=True,blank=True)
    avatar = models.ImageField(blank=True, null=True,upload_to='media/user/')
    description = models.CharField(null=True ,blank=True, max_length=500)
    follower = models.ManyToManyField('self',symmetrical=False,related_name='user_follower',blank=True)
    following = models.ManyToManyField('self',symmetrical=False,related_name='user_following',blank=True)

    def __unicode__(self):
        return self.user_name


class Tag(models.Model):
    tag = models.CharField(max_length=200, blank=True)

    def __unicode__(self):
        return self.tag
    def __str__(self):
        return self.tag

class CategoryManager(models.Manager):
    def get_new_category(self):
        query = self.get_queryset().order_by('-created_date')
        return query

    def get_hot_category(self):
        query=[]
        hot_topic = BaseTopic.objects.order_by('-created_date')
        query = self.get_queryset().prefetch_related(Prefetch('category_topic',queryset=hot_topic,to_attr='get_topic6'),\
                                                     'get_topic6__topic_picture')
        return query

class Category(models.Model):
    name = models.CharField(unique=True, max_length=20)
    description = models.CharField(max_length=100)
    involved = models.IntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    recommend = models.IntegerField(default=0)
    objects = CategoryManager()

    def __unicode__(self):
        return self.name
class FavoriteManager(models.Manager):
    def get_all_owner(self):
        arry=[]
        for i in self.get_queryset():
            arry.append(i.owner)
        return arry

class BaseTopicManager(models.Manager):
    def get_topics_by_cat(self,cat):
        return self.get_queryset().select_related('Mp3','created_by__common_user').\
            prefetch_related('forum_favorite_related__owner','tag','topic_reply__replyer',\
            'topic_picture',).filter(category=cat,status='P').order_by('-created_by')
    def get_topics_all_user(self):
        pass
    def archive_user_all_topic(self,uid):
        dates=set()
        dic={}
        dates = self.get_queryset().created_date
        for date in dates:
            query = self.get_queryset().filter(created_date=date, created_by=uid)
            dic.setdefault(date,[]).append(query)
        return dic

class PicManager(models.Manager):
    def get_first_pic(self):
        try:
            piclist = self.get_queryset()[0]
        except:
            piclist = None
        return piclist
class Mp3(models.Model):

    name = models.CharField(max_length=40)
    pic = models.CharField(max_length=300)
    url = models.CharField(max_length=300)
    def __unicode__(self):
        return self.name



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
    Mp3 = models.OneToOneField(Mp3,blank=True,null=True)
    #type = models.CharField(blank=True,max_length=20)
    objects = BaseTopicManager()

    def __unicode__(self):
        return self.title

class Picture(models.Model):
    topic = models.ForeignKey(BaseTopic, related_name='topic_picture')
    picture = models.ImageField(upload_to='media/')
    description = models.CharField(max_length=200)
    objects = PicManager()
    def __unicode__(self):
        return self.topic.title
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
        self.owner




class Favorite(Baseinvolved):
    event = GenericRelation('Event')
    objects = FavoriteManager()
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
                    event = Event(author=reply.replyer,event=reply,to_other=to_user,status=0)
                    event.save()
                except:
                    pass
    elif reply.replyer != reply.topic.created_by:
        event =Event(author =reply.replyer,event=reply,to_other =reply.topic.created_by,status=0)
        event.save()
@receiver(pre_delete,sender=BaseTopic,dispatch_uid='num2')
def delete_handler(sender,instance, **kwargs):
    topic = instance
    try:
        topic.category.involved-=1
        topic.category.save()
        pics=Picture.objects.filter(topic=topic)
        for pic in pics:
            print pic.picture.path
            os.remove(pic.picture.path)
    except Picture:
        pass



class Event(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    event = GenericForeignKey('content_type', 'object_id')
    author = models.ForeignKey(User, verbose_name=u"发起人")
    status = models.IntegerField()
    is_read = models.BooleanField(default=False, verbose_name=u'已读')
    submint_time = models.DateTimeField(auto_now_add=True, verbose_name=u'时间')
    to_other = models.ForeignKey(User, related_name="other", verbose_name=u"提到的人",null=True,blank=True)

    def __unicode__(self):
        return (self.author, self.event.topic, self.to_other)
