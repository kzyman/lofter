__author__ = 'Administrator'
from celery import shared_task

@shared_task
def add(x, y):
    return  x + y
def a(w):
    print w

