#-*- coding:utf-8 -*-
from django.conf.urls import url,include
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
    url(r'upload/$',upload , name='upload'),
    url(r'login/$',login,name='login'),
    url(r'get_user/$',get_user,name='get_user'),
    url(r'add_re/$',add_re,name='add_re'),
    url(r'register/$',register,),
    url(r'jcrop/$',jcrop,name='jcrop'),
    url(r'set_avatar/$',set_avata,name='set_avatar'),
    url(r'^get_topics/(?P<category>[\w]+)/$',get_topics,name='get_topics'),
    url(r'^get_topics_first/(?P<category>[\w]+)/(?P<topic_id>[\w]+?)/$',get_topics,name='get_topics_first'),
    url(r'^favorite/(?P<topic_id>[\w]+)/$',favorite,name='favorite'),
    url(r'^unfavorite/(?P<topic_id>[\w]+)/$',cancel_favorite,name='cancel_favorite'),
    url(r'post_setting/$',post_setting,name='setting'),
    url(r'reply/(?P<topic_id>[\w]+)/$',add_reply,name='add_reply'),
    url(r'get_setting/$',get_setting,name='get_setting'),
    url(r'^search/$', search, name='search'),
    url(r'^set_following/$', set_following, name='set_following'),
    url(r'^subscript/$', subscript, name='subscript'),
    url(r'^load_topics/$', load_topics, name='load_topics'),
    url(r'^get_div/$', get_div, name='get_div'),
    url(r'^get_captcha/$', get_captcha, name='get_captcha'),

]
#这里是我标注的测试
