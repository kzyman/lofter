__author__ = 'Administrator'
from celery import task
from models import *
@task
def notifly(event,user):
    try:
        self = LofterUser.objects.get(users=user.id)
        at_tem=self.follower.all()
        if at_tem:
            for to_user in at_tem:
                if to_user.user_name != self.user_name:
                    event1=Event(event=event,author=user,to_other=to_user.users,status=1)
                    event1.save()
    except LofterUser.DoesNotExist:
        pass









