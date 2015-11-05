from datetime import datetime, date, time, timedelta
import json
import uuid
import hmac
import hashlib
import base64
from apps.mentor.models import UserActivity
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


# App key + secret
import pytz

SINCH_APPLICATION_KEY = '7ecce9b0-b11d-48ef-9792-67a0467942d7'
SINCH_APPLICATION_SECRET = 'WKPpEbTsr025To67v0JKXA=='

userBase = dict()

from apps.user.models import Request

from datetime import timedelta as td


@login_required
def index(request):
    context = RequestContext(request)
    context_dict = {}
    user = request.user
    user_profile = user.user_profile
    template = None
    print "retrieving requests"

    if user_profile.is_mentor == True:
        # Update the user last seen, which essentially makes mentor ONLINE
        try:
            activity = UserActivity.objects.get(mentor=user)
            activity.last_seen = datetime.now(pytz.utc)
            activity.save()
        except ObjectDoesNotExist:
            activity = UserActivity()
            activity.mentor = user
            activity.last_seen = datetime.now(pytz.utc)
            user.save()
        template = "mentor/live.html"
    else:
        now = datetime.now(pytz.utc)
        min_dt = now - td(minutes=15)
        max_dt = now + td(minutes=15)
        req_objs = Request.objects.filter(menteeId_id=request.user.id, is_approved=True,
                                          dateTime__startswith=now.date())
        if req_objs:
            req_list = []
            print req_objs
            for obj in req_objs:
                print "obj.dateTime={0}".format(obj.dateTime)
                print "min_dt={0}".format(min_dt)
                print "max_dt={0}".format(max_dt)
                print "obj.dateTime.time()={0}".format(obj.dateTime.time())
                if obj.dateTime.date() == now.date() and min_dt.time() <= obj.dateTime.time() <= max_dt.time() \
                        and obj.is_completed == False:
                    mentor = User.objects.get(id=obj.mentorId_id)
                    status = 1
                    print obj
                    # We are adopting a POLLING technique on mentor's page and it's client's task to update last seen
                    # every 5 minutes
                    try:
                        if mentor.activity.last_seen < datetime.now(pytz.utc) - timedelta(minutes=2):
                            status = 0
                    except ObjectDoesNotExist:
                        # Simply mark mentor as offline if last seen doesnt not exist
                        status = 0

                    if now.time() < obj.dateTime.time():
                        # 0 => mentor is offline
                        # -1 => mentee has come earlier
                        status = -1

                    endTime = obj.dateTime + td(minutes=obj.duration)
                    req_list.append(
                        {'request_id': obj.id, 'date': obj.dateTime, 'startTime': obj.dateTime,
                         'endTime': endTime,
                         'duration': obj.duration,
                         'status': obj.is_approved,
                         'callType': obj.callType,
                         'req_date': obj.requestDate,
                         "mentor_name": mentor.get_full_name(),
                         "country": mentor.user_profile.country,
                         "mentor_id": mentor.id,
                         "mentor_pic": mentor.user_profile.picture,
                         "number": mentor.user_profile.contact,
                         "status": status})
            context_dict['req_list'] = req_list
        template = "mentee/live.html"

    return render_to_response(template, context_dict, context)


# Generate Sinch authentication ticket. Implementation of:
# http://www.sinch.com/docs/rest-apis/api-documentation/#Authorization
def getAuthTicket(user):
    userTicket = {'identity': {'type': 'username', 'endpoint': user['username']}, 'expiresIn': 3600,
                  'applicationKey': SINCH_APPLICATION_KEY, 'created': datetime.utcnow().isoformat()}
    userTicketJson = json.dumps(userTicket).replace(" ", "")
    userTicketBase64 = base64.b64encode(userTicketJson)
    digest = hmac.new(base64.b64decode(SINCH_APPLICATION_SECRET), msg=userTicketJson, digestmod=hashlib.sha256).digest()
    signature = base64.b64encode(digest)
    signedUserTicket = userTicketBase64 + ':' + signature
    return {'userTicket': signedUserTicket}


@login_required
def ticketHandler(request):
    user = {}
    user['username'] = 'user' + str(request.user.id)
    print request.user.id
    userTicket = getAuthTicket(user)
    return JsonResponse(userTicket)


def pingHandler(request):
    return JsonResponse({'hell': 'o'})


def getCallerInfo(request):
    user = User.objects.get(id=request.POST['userId'])
    return JsonResponse({'fullName': user.get_full_name(), 'picture': user.user_profile.picture})
