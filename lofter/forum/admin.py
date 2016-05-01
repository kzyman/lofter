#-*- coding:utf-8 -*-
from django.contrib import admin

# Register your models here.
from forum.models import *


admin.site.register(Category)
admin.site.register(Event)
admin.site.register(Tag)
admin.site.register(BaseTopic)
admin.site.register(LofterUser)
admin.site.register(Picture)
admin.site.register(Reply)
admin.site.register(Favorite)
