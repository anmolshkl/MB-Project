#from __future__ import absolute_import
from apps.user.models import Request
from django.contrib.auth.models import User
import datetime
import celery
from datetime import timedelta
from celery import shared_task
from django.core.mail import send_mail


@celery.decorators.periodic_task(run_every=datetime.timedelta(seconds=15))
#@shared_task
def mailme():
    print 'periodic_task'
    f = open('abc.txt','a+')
    f.write('hi there\n') # python will convert \n to os.linesep
    f.close() # you can omit in most cases as the destructor will call if

    one_hour_from_now = datetime.datetime.now() + timedelta(hours=1)

    #get all requests from start of platform time till next hour
    mailinglist = Request.objects.filter(dateTime__lte=one_hour_from_now)

    #exclude all requests before current time
    mailinglist2 = mailinglist.exclude(dateTime__lte=datetime.datetime.now())

    mailinglist3 = mailinglist2.filter(is_approved=1)

    for m in mailinglist:
        mentormailid = m.mentorId
        menteemailid = m.menteeId
        time = m.dateTime
        menteename = User.objects.get(username=menteemailid) 
        print mentormailid
        print menteemailid
        print menteename.first_name
        print menteename.last_name

        print time

        # Send email to mentor with meeting reminder
        email_subject = 'Meeting Reminder'
        email_body = "Hi, This mail is to remind you that you have a meeting with %s  %s at %s." % (menteename.first_name,menteename.last_name, time)   

        print email_body
        print "trying to send mail with reminder"
        #send_mail(email_subject, email_body, 'admin@mentorbuddy.in',[mentormailid], fail_silently=False)
        print "mail sent with activation key"



"""
q3 = q1.filter(pub_date__gte=datetime.date.today())
q1 = Entry.objects.filter(headline__startswith="What")
@celery.decorators.periodic_task(run_every=datetime.timedelta(seconds=5))
def remindermail():
    print 'periodic_task'

    one_hour_from_now = datetime.now() + timedelta(hours=1)
    mailinglist = Request.objects.filter(dateTime__lte==one_hour_from_now)
    print(mailinglist)

"""
    

    



