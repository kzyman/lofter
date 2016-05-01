#coding:utf-8
import uuid, os
import json
from PIL import Image
from django.shortcuts import render,redirect
from forum.models import *
from forum.forms import *
from django.utils import timezone
from django.utils.http import urlquote
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from forum.tasks import get_category1
def index(request):
    user = request.user

    categories = Category.objects.all()

    return render(request, 'forum/index.html', locals())
def category_a(request):
    categories = Category.objects.all()
    return render(request, 'forum/category.html', locals())
def get_user_inf(request,user_id):
    try:
        user = User.objects.select_related().get(pk=user_id)
    except User.DoesNotExist:
        return
    if user:
        article = user.author_topic.all()[:3]
        article_num = user.author_topic.count()
        like_num = user.forum_favorite_related.count()
        following_num = user.common_user.following.count()
    return HttpResponse(json.dumps({
        "articile":article,
        "artcle_num":article_num,
        "like_num":like_num,
        "following_num":following_num

    }),content_type="application/json")



def get_topics(request,category,topic_id=None):
    try:
        first_topic = BaseTopic.objects.get(pk=topic_id)
    except BaseTopic.DoesNotExist:
        first_topic =None
    category = Category.objects.select_related().get(pk=category)
    topics = category.category_topic.all()

    if first_topic:
        pass
    print first_topic
    forum = TxtForm()
    return render(request,'forum/topics.html',locals())
@login_required()
def favorite(request,topic_id):
    user = request.user
    if not user.is_authenticated():
        return HttpResponse(json.dumps({
            'success':0,
            'message':'user_not_login'
        }),content_type='application/json')
    try:
        topic_id = int(topic_id)
    except:
        topic_id = None
    topic = None
    if topic_id:
        try:
            topic = BaseTopic.objects.select_related('created_by').get(pk=topic_id)
        except BaseTopic.DoesNotExist:
            pass
    if not(topic_id and topic):
        return HttpResponse(json.dumps({
            'success':0,
            'message':'topic_not_exist'
        }),content_type='application/json')
   # if user.id == topic.created_by.id:
    #    return HttpResponse(json.dumps( {
     #       'success':0,
     #       'message':'can_not_favorite_your_topic'
      #      }),content_type='application/json')
    if Favorite.objects.filter(owner=user,involved_topic=topic).exists():
        return HttpResponse(json.dumps({
            'success': 0,
            'message': 'already_favorited'
        }), content_type='application/json')
    favorite = Favorite(owner = user,involved_topic=topic,created_time=timezone.now() )
    favorite.save()
        #notfing
    return HttpResponse(json.dumps({
        'success':1,
        'message':'cancel_favorite_success'
    }),content_type='application/json')
#@login_required()
def cancel_favorite(request,topic_id):
    user = request.user
    try:
        topic_id = int(topic_id)
    except:
        topic_id = None
    topic = None
    if topic_id:
        try:
            topic = BaseTopic.objects.select_related('created_by').get(pk=topic_id)
        except BaseTopic.DoesNotExist:
            pass
        print topic
    if not (topic_id and topic):
        return HttpResponse(json.dumps({
            'success': 0,
            'message': 'topic_not_exist'
        }), content_type='application/json')

    try:
        favorite = Favorite.objects.get(owner=user, involved_topic=topic)
    except Favorite.DoesNotExist:
        favorite = None
    print favorite
    if not favorite:
        return HttpResponse(json.dumps({
            'success': 0,
            'message': 'not_been_favorited'
        }), content_type='application/json')

    favorite.delete()
    return HttpResponse(json.dumps({
        'success':1,
        'message': 'cancel_favorite_success'
    }), content_type='application/json')

def add_category(request):
    if request.method =='POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('forum:category'))

    else:
        form = CategoryForm()

    return render(request, 'forum/add_category.html',locals())
def add_texttopic(request,category_id):
    user = request.user
    if request.method == 'POST':
        form = TxtForm(request.POST)
        category = Category.objects.get(pk=category_id)
        print category
        if form.is_valid():
            form=form.save(commit=False)
            form.category=category
            form.created_by =user
            form.save()

    return redirect(reverse('forum:get_topics',args=(category_id)))

def add_musictopic(request,category):
    if request.method == 'POST':
        form =MusicForm(request.Post)
        if form.is_valid():
            form.save(commit=False)

            return topic(request,category)
        else:
            print form.errors
    else:
        form=MusicForm()
    return render(request,'forum/add_musictopic.html',{'form':form})

def add_vediotopic(request,category):
    if request.method == 'POST':
        form =VedioForm(request.Post)
        if form.is_valid():
            form.save(commit=True)
            return topic(request,category)
        else:
            print form.errors
    else:
        form=VedioForm()
    return render(request,'forum/add_vediotopic.html',{'form':form})

def add_pictopic(request,category):
    user = request.user
    if request.method == 'POST':
        photoinfo = request.POST.get('photoinfo')
        conten  =request.POST.get('content')
        photoinfo = json.loads(photoinfo)
        for photo in photoinfo:
            items = photo.values()
            topic=BaseTopic.objects.create(created_by=user, content=conten,category=category)
            Picture.objects.create(picture=items[0],description=items[1],topic =topic)
        return redirect(reverse('forum:get_topics',args=(category)))

    else:
        form=PicForm()
    return render(request,'forum/add_pictopic.html',{'form':form})
#-----
#修改已经发布的topic
def edit_topic(request,topic_id):
    user =request.user
    now = timezone.now()
    topic=None
    if user.id != topic.created_by.id:
        return HttpResponse(json.dumps({
            'success':0,
            'message':'not_author',
        }), content_type='application/json')
    return HttpResponse(json.dumps({
            'success':1,
            'message':'ok',
        }), content_type='application/json')
    pass


@login_required
def get_new_num(request):
    user = request.user
    new_num = Event.objects.filter(to_other=user,is_read=False, is_deleted=False).count()
    return HttpResponse(new_num)
@login_required
def get_news(request):
    user=request.user
    news = Event.objects.filter(to_other=user, is_deleted=False).exclude()

#---------------------------
#topic reply part
#@login_required()

def add_reply(request,topic_id):
    user = request.user
    now = timezone.now()
    content = request.POST.get('photo')
    content=json.loads(content)
    print content
    for i in content:
        i=i.values()
        print i


    if content:
        topic =BaseTopic.objects.get(pk=topic_id)
        form = TxtForm()
        print topic
        #Reply.objects.create(content = content, replyer = user,submit_time = now,topic = topic)
        return  HttpResponse(json.dumps({"content":content}))
    return HttpResponse(json.dumps({"content":None}))
#---------
#File picture uploader
def upload(request):
    if request.method =='POST':
        files = request.FILES.get('file')
        with Image.open(files,'r') as pic:

            pic_id = uuid.uuid1()
            basepath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            print basepath
            pic.save(os.path.join(basepath,'media\\'+'%s.jpg' % pic_id))

            return HttpResponse(json.dumps({
                'id':'%s'%pic_id,
                'address':"/media/forum/media/%s.gif" %pic_id,
                }),content_type="application/json")
    else:
        return HttpResponse(505)








