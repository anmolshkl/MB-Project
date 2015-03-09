from datetime import datetime
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
from django.http import HttpResponse,HttpResponseRedirect
from django.http import JsonResponse


# App key + secret
SINCH_APPLICATION_KEY = '7ecce9b0-b11d-48ef-9792-67a0467942d7'
SINCH_APPLICATION_SECRET = 'WKPpEbTsr025To67v0JKXA=='

userBase = dict()

@login_required
def index(request):
	context = RequestContext(request)
	context_dict = {}
	user = request.user
	template = None

	if user.user_profile.is_mentor:
		template = "mentor/live.html"
	else:
		template = "mentee/live.html"

	return render_to_response(template,context_dict,context)

# Generate Sinch authentication ticket. Implementation of:
# http://www.sinch.com/docs/rest-apis/api-documentation/#Authorization
def getAuthTicket(user):
	print user
	print "in getAuthTicket"
	userTicket = { 'identity': {'type': 'username', 'endpoint': user['username']},'expiresIn': 3600,'applicationKey': SINCH_APPLICATION_KEY,'created': datetime.utcnow().isoformat() }
	print "in getAuthTicket 1"
	userTicketJson = json.dumps(userTicket).replace(" ", "")
	print "in getAuthTicket 2"
	userTicketBase64 = base64.b64encode(userTicketJson)
	print "in getAuthTicket 3"
	digest = hmac.new(base64.b64decode(SINCH_APPLICATION_SECRET), msg=userTicketJson, digestmod=hashlib.sha256).digest()
	print "in getAuthTicket 4"
	signature = base64.b64encode(digest)
	print "in getAuthTicket 5"
	signedUserTicket = userTicketBase64 + ':' + signature
	print signedUserTicket
	return {'userTicket': signedUserTicket}

@login_required
def loginHandler(request):
	user = {'username':request.POST['username'],'password':request.POST['password']}
	print user['username']
	print user['password']
	userTicket = getAuthTicket(user)
	print userTicket
	return JsonResponse(userTicket)


def pingHandler(request):
	return JsonResponse({'hell':'o'})