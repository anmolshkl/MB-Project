'''See this for this adapter design: http://stackoverflow.com/questions/19354009/
django-allauth-social-login-automatically-linking-social-site-profiles-using-th/19443127#19443127'''

from django.contrib.auth.models import User

from allauth.exceptions import ImmediateHttpResponse
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.http import HttpResponse


class SocialLoginAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        # This isn't tested, but should work
        try:
            user = User.objects.get(email=sociallogin.account.user.email)
            sociallogin.connect(request, user)
            # Create a response object
            response = HttpResponse()
            raise ImmediateHttpResponse(response)
        except Exception:
            pass
    '''
    def get_login_redirect_url(self, request):
        print "get_login_redirect_url"
        user = User.objects.get(email=sociallogin.account.user.email)
        user_profile = UserProfile.objects.get(user=user)
        if user_profile.is_new:
            login_url = "/user/newsuser/"
        else:
            loin_url = "/user/"
        return login_url
    '''