#-*- coding:utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
# Register your models here.
from forum.models import *
class TopicFilter(admin.SimpleListFilter):
    title = _(u'测试')
    parameter_name = u'测试的标题'
    def lookups(self, request, model_admin):
        return (('3',_(u'超过3个')),
                ('5',_(u'抄过5个')),
                )
    def queryset(self, request, queryset):
        if self.value() == '3':
            return queryset.filter(category__involved__gte=3)
        if self.value() =='5':
            return queryset.filter(category__involved__gte=5)
class TopicAdmin(admin.ModelAdmin):
    list_filter = ('category__name',TopicFilter)
admin.site.register(Category)
admin.site.register(Event)
admin.site.register(Tag)
admin.site.register(BaseTopic,TopicAdmin)
admin.site.register(LofterUser)
admin.site.register(Picture)
admin.site.register(Reply)
admin.site.register(Favorite)
admin.site.register(Mp3)

