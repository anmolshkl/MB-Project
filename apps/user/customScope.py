__author__ = 'anmol'

from social.backends.facebook import FacebookOAuth2
from social.backends.google import GoogleOAuth2



class CustomFacebookOAuth2(FacebookOAuth2):
    def get_scope(self):
        scope = super(CustomFacebookOAuth2, self).get_scope()
        print "inside scope"
        scope = scope + ['public_profile', 'user_birthday', 'user_education_history', 'user_location']
        return scope

class CustomGoogleOAuth2(GoogleOAuth2):
    def get_scope(self):
        scope = super(CustomGoogleOAuth2, self).get_scope()
        print "inside scope"
        print self.data
        scope = scope + ['profile']
        return scope
