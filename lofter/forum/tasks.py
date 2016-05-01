__author__ = 'kezhiyu'
from celery import task
from forum.models import Category
import os
@task(name='get-category-1')
def get_category1(x,y):
    c=Category.objects.all()
    a=open('/home/kezhiyu/task.txt','w')
    for i in c:
        a.write(i.name)
    a.close()

