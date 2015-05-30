from datetime import datetime, timedelta
from apps.user.models import Request
from celery import task
from django.contrib.auth.models import User
from django.core.mail import send_mail
import pytz


@task()
def add(x, y):
    return x + y

@task()
def printX():
    now = datetime.now(pytz.utc)
    request_objs = Request.objects.filter(is_approved=True, dateTime__lt=now+timedelta(minutes=30), dateTime__gt=now)

    return "x"

@task()
def notify():
    now = datetime.now(pytz.utc)
    request_objs = Request.objects.filter(is_approved=True, dateTime__lt=now+timedelta(minutes=30), dateTime__gt=now)
    for req in request_objs:
        mentor = User.objects.get(id=req.mentorId)
        mentee = User.objects.get(id=req.menteeId)

        send_mail('Its Working', 'Put your Email message here.', 'anmol@mentorbuddy.in', [mentor.email, mentee.email],
                  fail_silently=False)


