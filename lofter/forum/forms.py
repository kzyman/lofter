#-*- coding:utf-8 -*-
from django.forms import ModelForm
from forum.models import *
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

class MusicForm(ModelForm):
    class Meta:
        model = BaseTopic
        fields = ['title','content','music']

class CategoryForm(ModelForm):
    description = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Category
        fields = ['name','description']

class TxtForm(ModelForm):
    class Meta:
        model = BaseTopic
        fields =('title','content')

class PicForm(ModelForm):
    class Meta:
        model = BaseTopic
        fields = ('title','content',)

class VedioForm(ModelForm):
    class Meta:
        model = BaseTopic
        fields = ['title','content','vedio']

class ReplyForm(ModelForm):
    class Meta:
        model = Reply
        fields = ('content',)
class RegisterForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
class LofterUserForm(ModelForm):

    class Meta:
        model = LofterUser
        fields = ('user_name',)

class LoginForm(forms.Form):
    username = forms.CharField(min_length=6,max_length=12)
    password = forms.CharField(min_length=6,max_length=12)
    def clean(self):
        username = self.cleaned_data.get['username']
        password = self.cleaned_data.get['password']
        if username and password:
            self.user_cache = authenticate(username=username,password=password)
            if self.user_cache is None:
                raise forms.ValidationError(u'邮箱或者密码不正确')
            elif not self.user_cache.is_active:
                raise forms.ValidationError(u'邮箱锁定联系管理员')
        return self.cleaned_data

    def get_user(self):
        return self.user_cache

class SettingForm(ModelForm):

    avatar =forms.ImageField(required=False)
import itertools
def anyTrue(s,sequence):
    return True in itertools.imap(s,sequence)
def endsWith(s,*arg):
    return anyTrue(s.endswith,arg)
class PictureForm(forms.Form):
    picture = forms.CharField(max_length=500)
    description = forms.CharField(max_length=30)
    def clean_picture(self):
        cleaned_data = super(PictureForm, self).clean()
        picture = cleaned_data['picture']
        if picture.startswith('media/'):
            if not endsWith(picture,'.jpg', '.png', '.gif'):
                raise forms.ValidationError('图片格式必须为jpg、png或gif')
        else:
            raise forms.ValidationError('不能随意修改地址')
        return picture
