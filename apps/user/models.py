from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
# for django-allauth signals
from allauth.account.signals import user_logged_in, user_signed_up 
import datetime

#for upload_to
from django.utils.deconstruct import deconstructible
import os

from haystack.forms import SearchForm

#http://stackoverflow.com/questions/25767787/django-cannot-create-migrations-for-imagefield-with-dynamic-upload-to-value
@deconstructible
class PathAndRename(object):

    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        # set filename as random string
        filename = '{}.{}'.format(instance.user.username, ext)
        # return the whole path to the file
        return os.path.join(self.path, filename)

path_and_rename = PathAndRename("resume/")

class UserProfile(models.Model):

    """Associates the User with a 'Profile'."""

    # Stores username, password, first_name, last_name, email
    user = models.OneToOneField(User, related_name="user_profile", editable=False,
                                primary_key=True)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES,default='M',blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    contact = models.CharField(max_length=128, blank=True)
    college = models.CharField(max_length=128, blank=True)
    city = models.CharField(max_length=128, blank=True)
    state = models.CharField(max_length=128, blank=True)
    country = models.CharField(max_length=128, blank=True)
    about = models.TextField(blank=True)
    resume = models.FileField(upload_to=path_and_rename, null=True, blank=True)
    picture = models.CharField(max_length=128,blank=True, null=True) #Contains URL
    is_mentor = models.BooleanField(default=False)
    is_new = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    def full_name(self):
        return self.user.get_full_name() 

    def __unicode__(self):
        full_name = self.user.get_full_name()
        if full_name:
            return full_name
        else:
            return self.user.username

    class Meta:
        verbose_name = "User Profile"

    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            profile = UserProfile.objects.create(user=instance)


    models.signals.post_save.connect(create_user_profile, sender=User)

class SocialProfiles(models.Model):
    """Stores social profile urls of the user"""

    parent = models.OneToOneField(UserProfile, related_name="social_profiles",
                                  editable=False)
    #we may need other social urls for later use
    profile_url_facebook = models.URLField(max_length=256, blank=True,default='')
    profile_url_linkedin = models.URLField(max_length=256, blank=True,default='')
    profile_url_twitter  = models.URLField(max_length=256, blank=True,default='')
    profile_url_google = models.URLField(max_length=256, blank=True,default='')
    profile_url_github = models.URLField(max_length=256, blank=True,default='')

    profile_pic_url_facebook = models.URLField(max_length=256, blank=True,default='')
    profile_pic_url_linkedin = models.URLField(max_length=256, blank=True,default='')
    profile_pic_url_google = models.URLField(max_length=256, blank=True,default='')
    profile_pic_url_github = models.URLField(max_length=256, blank=True,default='')
    profile_pic_url_twitter  = models.URLField(max_length=256, blank=True,default='')
    def __unicode__(self):
        return u"Social Profiles - {0}".format(self.parent.full_name())

    class Meta:
        verbose_name = verbose_name_plural = "Social Profiles"


# Create your models here.@receiver ([user_signed_up, user_logged_in], sender=User)
@receiver([user_signed_up,user_logged_in])
def save_data(sender, **kwargs):
    ''' 
    things to do:
                1.create social profile for the user and populate it 
                2.let the adapter do its work of returning different login urls->dont need this now
    '''
    user = kwargs.pop('user')
    userProfile,usrprof_created= UserProfile.objects.get_or_create(user=user)
    socialProfiles, socprof_created = SocialProfiles.objects.get_or_create(parent=userProfile)
    
    #try to check whether user has any data provided by LinkedIn
    extra_data = None
    try:
        extra_data = user.socialaccount_set.filter(provider='linkedin')[0].extra_data
    except:
        pass
    if extra_data:
        socialProfiles.profile_url_linkedin = extra_data['public-profile-url']
        socialProfiles.profile_pic_url_linkedin = extra_data['picture-url']
        socialProfiles.save()


class MentorSearchForm(SearchForm):

    def no_query_found(self):
        return self.searchqueryset.all()

    def search(self):
        # First, store the SearchQuerySet received from other processing. (the main work is run internally by Haystack here).
        sqs = super(MentorSearchForm, self).search()

        # if something goes wrong
        if not self.is_valid():
            return self.no_query_found()

        # you can then adjust the search results and ask for instance to order the results by title
        #sqs = sqs.order_by(city)

        return sqs