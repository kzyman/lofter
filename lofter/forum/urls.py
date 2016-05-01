#-*- coding:utf-8 -*-
from django.conf.urls import url
from forum.views.user import *
from forum.views.views import *

urlpatterns =[
    url(r'^index/$', index ,name='index',),
    url(r'^category/$',category_a,name='category'),
    #url(r'^topic/(?P<category_name>[\w]+)/$',topic,name='topic'),
    url(r'^add_category/$',add_category, name='add_category'),
    url(r'^add_txttopic/(?P<category_id>[\w]+)/$',add_texttopic,name='add_texttopic'),
    url(r'^add_musictopic/(?P<category>[\w]+)/$',add_musictopic,name='add_musictopic'),
    url(r'^add_pictopic/(?P<category>[\w]+)/$',add_pictopic,name='add_pictopic'),
    url(r'^add_vediotopic/(?P<category>[\w]+)/$',add_vediotopic,name='add_vediotopic'),
    url(r'^get_user_inf/(?P<user_id>[\w]+)/$',get_user_inf,name='get_user_inf'),
    url(r'upload/$',upload , name='upload'),
    url(r'login/$',login,),
    url(r'register/$',register,),
    url(r'^get_topics/(?P<category>[\w]+)/$',get_topics,name='get_topics'),
    url(r'^get_topics_first/(?P<category>[\w]+)/(?P<topic_id>[\w]?)/$',get_topics,name='get_topics_first'),
    url(r'^favorite/(?P<topic_id>[\w]+)/$',favorite,name='favorite'),
    url(r'^unfavorite/(?P<topic_id>[\w]+)/$',cancel_favorite,name='cancel_favorite'),
    url(r'post_setting/$',post_setting,name='setting'),
    url(r'reply/(?P<topic_id>[\w]+)/$',add_reply,name='add_reply'),
    url(r'get_setting/$',get_setting,name='get_setting'),]
