#coding:utf-8
__author__ = 'Kezhiyu'
import uuid, os, json,re
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
'''
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        user_name = request.POST.get('user_name')
        form = RegisterForm({'username':username,'password':password,'email':email})
        user =User()
        user.username=username
        user.set_password(password)
        user.email=email
        user.save()
        lof_user = LofterUser()
        lof_user.user=user
        lof_user.user_name= user_name
        lof_user.save()
        newUser =auth.authenticate(username=username,password=password)
        if newUser:
            auth.login(request,newUser)
            return HttpResponseRedirect('forum/index')
    else:
        return render(request,'user/register.html')
    return render(request,'user/register.html',locals())
'''
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
            return HttpResponseRedirect('forum/index')
        else:
            print form.errors,lof_form.errors
    else:
        form=RegisterForm()
        lof_form =LofterUserForm()
    return render(request,'user/register.html',locals())


def get_setting(request):
    return render(request,'user/setting.html')
@csrf_exempt
def post_setting(request):
    if request.method =='POST':
        files = request.FILES.get('file')
        print files
        basepath = os.path.dirname(os.path.dirname(__file__))
        a= os.path.join(basepath,'media/'+'sa.jpg')
        print a
        pic_id = uuid.uuid1()
        x=Image.open(files,'r')


        x.save(os.path.join(basepath,'media/'+'%s.gif' % pic_id))

        #x=Picture(topic=topic,picture=files[0])
        #x.save()
       # print x
        return HttpResponse(json.dumps({
            'address':"/media/forum/media/%s.gif" % pic_id,
        }),content_type="application/json")
    else:
        return get_setting(request)


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                auth.login(request,user)
                return HttpResponseRedirect('/forum/index')
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




