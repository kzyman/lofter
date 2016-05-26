#coding:utf-8
from django.db import connection
from django.template import RequestContext
from django.shortcuts import render_to_response
import uuid, os
import json
from PIL import Image
from django.db.models import Q
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from forum.models import *
from forum.forms import *
from django.utils import timezone
from django.utils.http import urlquote
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from forum.task import *
from django.core.cache import cache

def index(request):
    user = request.user
    categories = Category.objects.prefetch_related('category_topic__topic_picture').all()
    return render_to_response('forum/index.html',locals(),context_instance=RequestContext(request))
def subscript(request):
    return render(request,'forum/reminder.html',{'cats':Category.objects.all()[:10]})
def get_div(request):
    user = request.user
    id = request.GET.get('id')
    topic = BaseTopic.objects.select_related('created_by','Mp3').prefetch_related('tag','topic_picture').get(pk=id)
    if topic:
        img_num = topic.topic_picture.all().count()
        print img_num
        return render(request,'forum/get_div.html',locals())
    else:
        return HttpResponse(u'文章不存在')

@login_required
def set_following(request):
    user=request.user
    if request.method =='POST':
        following_id = request.POST.get('id')
        following = LofterUser.objects.get(pk=following_id)
        youself = LofterUser.objects.get(users=user)
        if following != youself:
            if not youself.following.filter(pk=following_id).exists():
                youself.following.add(following)
                following.follower.add(youself)
                request.session['user-'+following.users.id]=True
                print following,youself
                return HttpResponse('ok')
            else:
                return HttpResponse('already')
        else:
            return HttpResponse('false')

@login_required
def search(request):
    if request.method =='GET':
        inpute_word = request.GET['search']
        if inpute_word:
             cat_list,user_list=suggestion(inpute_word)
             print user_list
    return render(request,'forum/reminder.html',{'cats':cat_list,'users':user_list})

def suggestion(input_word=None):
    if input_word:
        cat_list = Category.objects.filter(name__icontains=input_word)
        user_list = LofterUser.objects.filter(user_name__icontains=input_word)

    return  cat_list,user_list
@login_required
def category_a(request):
    categories = Category.objects.get_hot_category()
    return render(request, 'forum/category.html', locals())
def load_topics(request):
    user=request.user
    if request.method == 'POST':
        category = request.POST.get('id')
        num = int(request.POST.get('num'))
        request_num = int(request.POST.get('request_num'))#display page_num_list
        pages = int(request.POST.get('pages'))#calculate_topic_position
        num=int(num)
        pages_object_num = (pages-1)*12
        print num
        print pages_object_num

        if num>4:
            topics = BaseTopic.objects.get_topics_by_cat(category)[pages_object_num+request_num*4:pages_object_num+request_num*4+4] #请求次数×4 再加上不同页数减去前一页去掉前面浏览的个数
        else:
            topics = BaseTopic.objects.get_topics_by_cat(category)[pages_object_num:pages_object_num+num]
        print topics
    return render(request,'forum/load-topics.html',locals())
@login_required
def get_topics(request,category,topic_id=None,pages=1):
    seq=[]
    user=request.user
    pages=pages
    try:
        first_topic = BaseTopic.objects.get(pk=topic_id)
    except BaseTopic.DoesNotExist:
        first_topic =None
    category = Category.objects.get(pk=category)
    topics_num = BaseTopic.objects.filter(category=category).count()
    active_users = User.objects.select_related('common_user').filter(author_topic__category=category).\
        order_by('author_topic__created_date')
    for u in active_users:
        if u not in seq:
            seq.append(u)
    if first_topic:
        pass
    forum = TxtForm()
    return render(request,'forum/topics.html',locals())
@login_required
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
            topic = BaseTopic.objects.get(pk=topic_id)
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
    return HttpResponse(json.dumps({
        'success':1,
        'message':'cancel_favorite_success'
    }),content_type='application/json')
@login_required
def cancel_favorite(request,topic_id):
    user = request.user
    print user
    try:
        topic_id = int(topic_id)
    except:
        topic_id = None
    topic = None
    if topic_id:
        try:
            topic = BaseTopic.objects.get(pk=topic_id)
        except BaseTopic.DoesNotExist:
            pass
        print topic
    if not (topic_id and topic):
        return HttpResponse(json.dumps({
            'success': 0,
            'message': 'topic_not_exist'
        }), content_type='application/json')

    try:
        favorite = Favorite.objects.filter(owner=user, involved_topic=topic)
    except Favorite.DoesNotExist:
        favorite = None
    print favorite
    if not favorite:

        return HttpResponse(json.dumps({
            'success': 0,
            'message': 'not_been_favorited'
        }), content_type='application/json')
    for fa in favorite:
        fa.delete()
    return HttpResponse(json.dumps({
        'success':1,
        'message': 'cancel_favorite_success'
    }), content_type='application/json')
@login_required
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
    form=TxtForm()
    if request.method == 'POST':
        form = TxtForm(request.POST)
        category = Category.objects.get(pk=category_id)
        print category
        if form.is_valid():
            form=form.save(commit=False)
            form.category=category
            form.created_by =user
            form.save()
            category.involved+=1
            category.save()
            t,_=Tag.objects.get_or_create(tag=category.name)
            form.tag.add(t)
        return redirect(reverse('forum:get_topics',args=(category_id)))
    else:
        return render(request,'forum/add_txttopic.html',locals())

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
    if request.method == 'POST':
        form =PicForm(request.POST)
        if form.is_valid():
            form.save(commit=True)

            return topic(request,category)
        else:
            print form.errors
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
def edit_topic():

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

def add_reply(request,topic_id=None):
    user = request.user
    now = timezone.now()
    content = request.POST.get('content')
    if content:
        print content
    return HttpResponse('OK')


def add_re(request):
    user = request.user
    now = timezone.now()
    content = request.POST.get('content')
    a=json.loads(content)
    for i in a:
        print i['subs'],i['img']




    '''if content:
        topic =BaseTopic.objects.get(pk=topic_id)
        form = TxtForm()
        print topic
        Reply.objects.create(content = content, replyer = user,submit_time = now,topic = topic)
        return  HttpResponse(json.dumps({"content":content}))'''
    return HttpResponse(json.dumps({"content":None}))
#---------
#File picture uploader
def upload(request):
    if request.method =='POST':
        files = request.FILES.get('file')
        pic=Image.open(files,'r')
        print pic
        pic_id = uuid.uuid1()
        basepath = os.path.dirname(os.path.dirname(__file__))
        pic.save(os.path.join(basepath,'media\\'+'%s.gif' % pic_id))

        return HttpResponse(json.dumps({
            'id':'%s'%pic_id,
            'address':"/media/forum/media/%s.gif" %pic_id,
        }),content_type="application/json")
    else:
        return HttpResponse(505)








