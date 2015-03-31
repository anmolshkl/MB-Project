from datetime import datetime, date, time
import json
import uuid
import hmac
import hashlib
import base64
from django.contrib.auth.models import User
from apps.user.models import UserProfile
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse


# App key + secret
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
    template = None

    if user.user_profile.is_mentor:
        template = "mentor/live.html"
    else:
        today = datetime.now()
        today_min = datetime.combine(date.today(), time.min)
        today_max = datetime.combine(date.today(), time.max)
        req_objs = Request.objects.filter(menteeId_id=request.user.id, is_approved=True,
                                          dateTime__range=(today_min, today_max))
        if req_objs:
            req_list = []
            for obj in req_objs:
                mentor = User.objects.get(id=obj.mentorId_id)
                endTime = obj.dateTime + td(minutes=obj.duration)
                req_list.append({'request_id': obj.id, 'date': obj.dateTime.date(), 'startTime': obj.dateTime.time(),
                                 'endTime': endTime.time,
                                 'duration': obj.duration,
                                 'status': obj.is_approved,
                                 'callType': obj.callType, 'req_date': obj.requestDate,
                                 "mentor_name": mentor.get_full_name(), "country": mentor.user_profile.country,
                                 "mentor_id": mentor.id, "mentor_pic": mentor.user_profile.picture})
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