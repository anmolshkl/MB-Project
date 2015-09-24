from django.shortcuts import redirect, render_to_response
from django.template import RequestContext

__author__ = 'anmol'


class UserAuthMiddleware(object):
    # this middleware just checks whether the user is authorized to proceed ahead or not
    def process_request(self, request):
        if request.user and request.user.is_authenticated():
            user = request.user
            if user.user_profile.is_new and user.is_superuser == False:
                return render_to_response('user/selectV2.html', {}, context_instance=RequestContext(request))

        return None