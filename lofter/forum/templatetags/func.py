__author__ = 'Administrator'
from django import template
from forum.models import *
from  forum.forms import ReplyForm
register = template.Library()

@register.inclusion_tag('forum/reminder.html')
def get_reminder():
    return{'cats':Category.objects.all()[:10]}