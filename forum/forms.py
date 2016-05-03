#-*- coding:utf-8 -*-
from django.forms import ModelForm
from forum.models import *
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from DjangoUeditor.forms import UEditorField
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


class PictureForm(forms.Form):
    description=UEditorField("描述",initial="",width=550,height=400)


