#coding:utf-8
__author__ = 'Kezhiyu'
import uuid, os, json,re,random,cStringIO,string
import Image,ImageDraw,ImageFont,ImageFilter
from django.db import connection
from django.db.models import Count
from django.core.urlresolvers import reverse
from forum.models import LofterUser
from PIL import Image
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render,redirect,render_to_response
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.conf import settings
from forum.forms import LoginForm, SettingForm,RegisterForm,LofterUserForm
from django.views.decorators.csrf import csrf_exempt
from forum.models import *
from forum.views.views import *
from  django.core import serializers

def register(request):
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        lof_form = LofterUserForm(data=request.POST)
        if form.is_valid() and lof_form.is_valid():
            user1=form.save()
            user1.set_password(user1.password)
            user1.save()
            lof_form=lof_form.save(commit=False)
            lof_form.users = user1
            lof_form.save()
            return HttpResponseRedirect(reverse('forum:index'))
        else:
            print form.errors,lof_form.errors
    else:
        form=RegisterForm()
        lof_form =LofterUserForm()
    return render(request,'user/register.html',locals())
def get_user(request):
    img_list=[]
    a = request.GET['id']
    info = request.session.get('user-'+a)
    if info :
        following = info['following_num']
        article =info['article_num']
        favorite = info['favorite_num']
        img_list = info['img'] or []
        avatar = info['avatar'] or None
        is_following = info.get('is_following')
        print is_following
    else:
        user=LofterUser.objects.get(users=a)
        following = user.following.count()
        avatar = user.avatar.url or None
        is_following = LofterUser.objects.get(users=a).following.exists()
        article = BaseTopic.objects.filter(created_by=a).count()
        favorite = Favorite.objects.filter(owner=a).count()
        hot_img = Picture.objects.filter(topic__created_by=a).annotate(favor_num=Count \
            ('topic__forum_favorite_related')).order_by('favor_num')[:3] or []
        if hot_img:
            for img in hot_img:
                img_list.append(img.picture.url)
        request.session['user-'+a]={
            'following_num':following,
            'article_num':article,
            'favorite_num':favorite,
            'img':img_list,
            'avatar':avatar,
            'is_following':is_following}

        # print connection.queries

    return  HttpResponse(json.dumps({
        'following_num':following,
        'article_num':article,
        'favorite_num':favorite,
        'img':img_list,
        'avatar':avatar,
        'is_following':is_following
    }),content_type="application/json")
def jcrop(request):
    user = request.user
    return render(request,'forum/jcrop.html',locals())
@login_required
def get_setting(request):
    user=request.user
    return render(request,'user/setting1.html',locals())

def post_setting(request):
    if request.method =='POST':
        files = request.FILES.get('file')
        pic=Image.open(files,'r')
        width,height = pic.size
        print width,height
        pic_id = uuid.uuid1()
        if width<260 or height<200:
            return HttpResponse(json.dumps({
                'error':u"必须大于140像素"
            }),content_type="application/json")
        if width>height+50:
            size = (440,200)

        else:
            size = (260,350)
        x,y = size
        pic.thumbnail(size,Image.ANTIALIAS)
        pic.save(settings.MEDIA_PATH+'/%s.gif' % pic_id)

        return HttpResponse(json.dumps({
            'address':"/media/media/%s.gif" %pic_id,
            'width':x,
            'height':y,
        }),content_type="application/json")
    else:
        return get_setting(request)
@login_required
def set_avata(request):
    user = request.user
    content = json.loads(request.POST.get('content'))
    if content:
        print content
        avatar1 = content[0]['avatar']
        width = content[0]['width']
        height = content[0]['height']
        left = content[0]['left']
        top = content[0]['top']
        box=(left,top,left+width,height+top)
        a,b,c,pic1 = avatar1.split('/')
        pic_path = settings.MEDIA_PATH+'/%s' % pic1
        print pic_path
        pic=Image.open(pic_path,'r')
        print pic
        pic.crop(box).save(pic_path)
        LofterUser.objects.update_or_create(users=user,defaults={'avatar':avatar1,'user_name':u'测试看看1'})
        return HttpResponse("OK")
    else:
        return HttpResponse('NO')
def get_captcha(request):
    image= Image.new("RGB",(117,49),(255,255,255))
    font_file = settings.STATIC_PATH+"/forum/font/FreeMonoBold.ttf"
    font= ImageFont.truetype(font_file,36)
    draw = ImageDraw.Draw(image)
    rand_text = ''.join(random.sample(string.letters+string.digits,4))
    draw.text((7,0),rand_text,fill=(0,0,0),font=font)
    del draw
    request.session['captcha'] = rand_text.lower()
    buf = cStringIO.StringIO()
    image.save(buf,'jpeg')
    return HttpResponse(buf.getvalue(),'image/jpeg')

def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/forum/index')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        captcha = request.POST.get('captcha').lower()
        captcha_session = request.session.get('captcha')
        user = authenticate(username=username, password=password)
        if user and captcha == captcha_session:
            if user.is_active:
                auth.login(request,user)
                return HttpResponse(json.dumps({
                    'success':1,
                    'url':reverse('forum:index'),
                }),content_type='application/json')
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request,'user/login.html')



@login_required
def logout(request):
    auth.logout(request)
    return redirect('forum/index')
def test(request):
    content={}
    if request.method == 'POST':
        file = request.FILES.get("Filedata",None)
        content["savepath"] = file
    return render(request,'user/test.html')




